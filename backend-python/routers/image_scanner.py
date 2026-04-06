from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
from PIL import Image

router = APIRouter()

# 1. Load the Brain ONCE when the server starts
print("🧠 Loading SENTIN-AI Vision Model... Please wait.")
model = load_model("models/sentin_vision_model.keras")
print("✅ Vision Model Loaded!")




@router.post("/scan-screenshot")
async def scan_screenshot(file: UploadFile = File(...)):
    try:
        # 2. Read the uploaded file into temporary memory
        contents = await file.read()
        
        # 3. Open the image using Pillow (PIL)
        img = Image.open(io.BytesIO(contents))
        
        # 4. Force the uniform: Make sure it has RGB colors and is exactly 224x224
        img = img.convert("RGB")
        img = img.resize((224, 224))
        
        # 5. Color to Math translation
        img_array = image.img_to_array(img)
        
        # 6. The "Tray" Trick (Wrap it in a batch of 1)
        img_batch = np.expand_dims(img_array, axis=0)
        
        # 7. Ask the AI for its guess!
        prediction = model.predict(img_batch)
        score = float(prediction[0][0]) # Convert to standard Python number for JSON
        
        # 8. Calculate the final English results
        is_phishing = score >= 0.5
        confidence = score * 100 if is_phishing else (1 - score) * 100
        
        # 9. Send the JSON package back to the React Frontend!
        return {
            "success": True,
            "is_phishing": is_phishing,
            "confidence_percentage": round(confidence, 2),
            "message": "Threat Detected!" if is_phishing else "Website is Safe."
        }
        
    except Exception as e:
        # If anything breaks (like uploading a PDF instead of an image), don't crash the server!
        raise HTTPException(status_code=500, detail=str(e))