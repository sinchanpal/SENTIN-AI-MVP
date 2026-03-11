from fastapi import FastAPI
from pydantic import BaseModel
import joblib

#! to run this file use command : uvicorn main:app --reload
app = FastAPI()

# 1. Load the saved "brain" into memory when the server starts
model = joblib.load("spam_model.joblib")
vectorizer = joblib.load("vectorizer.joblib")


# This tells Python exactly what shape of data to expect from Node.js
class TextInput(BaseModel):
    text: str


@app.post("/analyze-text")
def analyze_text(data: TextInput):
    print(f"Python recieved this text : {data.text}")

    # ---------------------------------------------------------
    # DUMMY AI LOGIC
    # ---------------------------------------------------------

    # 2. Convert the incoming React text using the saved Vectorizer
    input_features = vectorizer.transform([data.text])

    # 3. Make the prediction (Returns an array, e.g., [0] or [1])
    prediction = model.predict(input_features)

    # 4. Map the ML result (0 = Spam, 1 = Ham) to the React UI logic
    if prediction[0] == 0:
        threat = "High"
        reason = "Spam/Malicious content detected by ML Model"
    else:
        threat = "Low"
        reason = "Looks Safe. No spam detected."

    # Send the result back to Node.js
    return {"threat_level": threat, "reason": reason}
