import streamlit as st
from model import load_models, predict_health_risk
from llm import  generate_descriptive_answer
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Load saved models
vectorizer, clf_model, reg_model = load_models()

st.title("🩺 MedNote AI - Health Risk Predictor")
st.write("Enter a medical note or description below to predict risk level and percentage.")

user_input = st.text_area("🧾 Doctor Note / Patient Description")

if st.button("Predict & Describe"):
    if user_input.strip():
        label, score = predict_health_risk(user_input, vectorizer, clf_model, reg_model)
        st.success(f"**Predicted Risk Label:** {label}")
        st.info(f"**Predicted Risk Score:** {score}%")
        
        # Initialize the Gemini model
        
        
        description = generate_descriptive_answer(user_input, label, score)
        st.write("### Detailed Explanation:")
        description = "\n".join(line.strip() for line in description.splitlines() if line.strip())
        st.markdown(description, unsafe_allow_html=False)
    else:
        st.warning("Please enter a valid description.")
