# 🛡️ SENTIN-AI: Multimodal Cybersecurity Dashboard

SENTIN-AI is a comprehensive, full-stack cybersecurity application designed to detect phishing attempts, malicious links, and forged websites. Moving beyond traditional "Black Box" machine learning, SENTIN-AI utilizes **Explainable AI (XAI)** to not only detect threats but also provide users with transparent, real-time visual and linguistic explanations for its decisions.

## ✨ Key Features & AI Models

SENTIN-AI analyzes threats across three distinct vectors:

1. **Text Scanner (NLP)** * **Model:** Multinomial Naive Bayes (MultinomialNB) with TF-IDF Vectorization.
   * **XAI:** Extracts and displays the highest-risk keywords that triggered the spam alert using Log-Probability Likelihood ratios.
2. **URL Scanner (Structural Analysis)**
   * **Model:** Random Forest Classifier.
   * **XAI:** Utilizes **SHAP** (SHapley Additive exPlanations) to output the top 3 structural anomalies (e.g., unusual folder depth, IP usage) that flagged the link.
3. **Visual Scanner (Computer Vision)**
   * **Model:** MobileNetV2 (Fine-tuned Custom Neural Network).
   * **XAI:** Generates a **Grad-CAM** Heatmap, overlaying a glowing heatmap onto the user's uploaded screenshot to show exactly which UI elements (logos, inputs, buttons) the AI deemed suspicious.

## 🏗️ System Architecture

The application is built on a scalable microservice architecture:
* **Frontend:** React.js + Tailwind CSS (Dark-mode UI)
* **Main Backend:** Node.js / Express (Traffic controller & file routing)
* **AI Engine:** Python / FastAPI (Dedicated high-speed machine learning microservice)

## 🚀 How to Run Locally

To run this project on your local machine, you will need to start all three servers. Open three separate terminal windows and follow the steps below:

### 1. The Python AI Engine
Navigate to the Python backend, set up a virtual environment, install the AI dependencies, and start the FastAPI server:
Bash
cd backend-python
python -m venv venv

### Activate the virtual environment:
### On Windows: venv\Scripts\activate


pip install -r requirements.txt
uvicorn main:app --reload


### 2. The Node.js Backend
Navigate to the Node backend, install packages, and start the server:

Bash
cd backend-node
npm install
npm start


### 3. The React Frontend
Navigate to the frontend folder, install packages, and spin up the UI:

Bash
cd frontend
npm install
npm run dev
