from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import base64
from PIL import Image
import matplotlib.cm as cm

router = APIRouter()

# 1. Load the Brain ONCE when the server starts
print("🧠 Loading SENTIN-AI Vision Model... Please wait.")
model = load_model("models/sentin_vision_model.keras")
print("✅ Vision Model Loaded!")

# ==========================================
# ? 2. XAI HELPER FUNCTIONS (The Detective & Artist)
# ==========================================


# ? This function uses TensorFlow's GradientTape to calculate which parts of the image were most influential in the model's decision. It produces a heatmap that highlights these areas.
def make_gradcam_heatmap(img_array, model):
    """Calculates where the AI is looking using GradientTape."""
    with tf.GradientTape() as tape:
        # Step through the layers manually
        x = model.layers[0](img_array)  # Rescaling
        visual_features = model.layers[1](x)  # MobileNetV2
        tape.watch(visual_features)

        preds = visual_features
        for layer in model.layers[2:]:
            preds = layer(preds)

        score = preds[:, 0]

    # Calculate gradients
    grads = tape.gradient(score, visual_features)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Calculate heatmap
    visual_features = visual_features[0]
    heatmap = visual_features @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # Normalize heatmap
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()


# ? This function takes the original image and the heatmap, blends them together, and converts it to a Base64 string that can be easily sent back to the frontend for display.
def get_heatmap_base64(original_img, heatmap, alpha=0.6):
    """Blends the heatmap onto the image and converts it to a Base64 string."""
    # 1. Convert heatmap to RGB colors (Jet scheme)
    heatmap = np.uint8(255 * heatmap)
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap]

    # 2. Resize heatmap to match original image size
    jet_heatmap = Image.fromarray(np.uint8(jet_heatmap * 255))
    jet_heatmap = jet_heatmap.resize(original_img.size, resample=Image.BILINEAR)

    # 3. Blend the images
    jet_heatmap = np.array(jet_heatmap)
    original_np = np.array(original_img)
    
    # Formula: (Heatmap * Intensity) + (Original * Remainder)
    # This ensures the total value NEVER exceeds 255.
    superimposed_img = (jet_heatmap * alpha) + (original_np * (1 - alpha))

    # 4. Convert back to PIL Image
    final_img = Image.fromarray(np.uint8(np.clip(superimposed_img, 0, 255)))

    # 5. TRANSLATION: Save to memory buffer and encode to Base64 string
    buffered = io.BytesIO()
    final_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{img_str}"


# ==========================================
# ? 3. THE API ENDPOINT
# ==========================================


@router.post("/scan-screenshot")
async def scan_screenshot(file: UploadFile = File(...)):
    try:
        # 2. Read the uploaded file into temporary memory
        contents = await file.read()

        # 3. Open the image using Pillow (PIL)
        img = Image.open(io.BytesIO(contents))

        # 4. Force the uniform: Make sure it has RGB colors and is exactly 224x224
        img = img.convert("RGB")

        original_size_img = img.copy()  # Keep a copy for the high-quality heatmap!

        img = img.resize((224, 224))

        # 5. Color to Math translation
        img_array = image.img_to_array(img)

        # 6. The "Tray" Trick (Wrap it in a batch of 1)
        img_batch = np.expand_dims(img_array, axis=0)

        # 7. Ask the AI for its guess!
        prediction = model.predict(img_batch)
        score = float(prediction[0][0])  # Convert to standard Python number for JSON

        # 8. Calculate the final English results
        is_phishing = score >= 0.5
        confidence = score * 100 if is_phishing else (1 - score) * 100

        #? --- XAI LOGIC ---
        heatmap_base64 = None
        if is_phishing:
            # Generate the heatmap math
            heatmap_math = make_gradcam_heatmap(img_batch, model)
            # Create the glowing image string
            heatmap_base64 = get_heatmap_base64(original_size_img, heatmap_math)

        # 9. Send the JSON package back to the React Frontend!
        return {
            "success": True,
            "is_phishing": is_phishing,
            "confidence_percentage": round(confidence, 2),
            "message": "Threat Detected!" if is_phishing else "Website is Safe.",
            "heatmap": heatmap_base64 # This will be the long Base64 string or null
        }

    except Exception as e:
        # If anything breaks (like uploading a PDF instead of an image), don't crash the server!
        raise HTTPException(status_code=500, detail=str(e))
