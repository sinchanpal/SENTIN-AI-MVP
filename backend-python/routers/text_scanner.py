from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import numpy as np

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("punkt_tab")  # Needed for newer NLTK versions

ps = PorterStemmer()

router = APIRouter()


# 2. Load the models
try:
    tfidf = pickle.load(open("models/vectorizer.pkl", "rb"))
    model = pickle.load(open("models/spam_model.pkl", "rb"))
    print("✅ Text AI Models Loaded Successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    # Filter: Keep only alphanumeric, remove stopwords and punctuation
    y = []
    for i in text:
        if i.isalnum():
            if i not in stopwords.words("english") and i not in string.punctuation:
                y.append(ps.stem(i))  # Apply stemming (e.g., "winning" -> "win")

    return " ".join(y)


# This tells Python exactly what shape of data to expect from Node.js
class TextInput(BaseModel):
    text: str


@router.post("/analyze-text")
def analyze_text(data: TextInput):

    try:

        # print(f"Python recieved this text : {data.text}")

        # 1st apply transform_text on the message
        input_text = transform_text(data.text)

        # 2. Convert the incoming React text using the saved Vectorizer
        input_vectorized_text = tfidf.transform([input_text])

        # 3. Make the prediction (Returns an array, e.g., [0])
        prediction = model.predict(input_vectorized_text)

        # 4. Map the ML result (0 = Spam, 1 = Ham) to the React UI logic
        if prediction[0] == 1:
            threat = "High"

            # Get the vocabulary from the TF-IDF vectorizer
            feature_names = tfidf.get_feature_names_out()

            # MultinomialNB stores log-probabilities of features
            # model.feature_log_prob_[0] -> Probabilities for Ham
            # model.feature_log_prob_[1] -> Probabilities for Spam
            ham_log_probs = model.feature_log_prob_[0]
            spam_log_probs = model.feature_log_prob_[1]

            # We want to see which words in THIS message have the
            # highest (Spam Prob - Ham Prob) difference
            words_in_message = list(set(input_text.split()))  # Unique words only
            word_impacts = []

            for word in words_in_message:
                if word in feature_names:
                    # Find where this word sits in the AI's dictionary
                    idx = np.where(feature_names == word)[0][0]

                    # Calculate how much more "Spammy" this word is than "Safe"
                    # In log space, subtraction is like division
                    spam_score = spam_log_probs[idx] - ham_log_probs[idx]
                    word_impacts.append((word, spam_score))

            # Sort by highest spam score and pick the top 3
            word_impacts.sort(key=lambda x: x[1], reverse=True)
            top_flags = [item[0] for item in word_impacts[:5]]

            if top_flags:
                reason = f"Flagged due to high-risk keywords: {', '.join(top_flags)}. These words appear significantly more often in phishing content."
            else:
                reason = "The overall message structure matches known spam patterns."

        else:
            threat = "Low"
            reason = "Looks Safe. No spam detected."

        # Send the result back to Node.js
        return {"threat_level": threat, "reason": reason}

    except Exception as e:
        print(f"Text Analysis Error: {e}")
        raise HTTPException(
            status_code=500, detail="Internal Server Error during text analysis"
        )
