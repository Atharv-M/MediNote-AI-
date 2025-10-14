import streamlit as st
from tools.model import load_models, predict_health_risk
from utils.llm import generate_descriptive_answer
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Load saved models
vectorizer, clf_model, reg_model = load_models()

# Sidebar instructions
st.sidebar.header("📝 Note Guidelines")
st.sidebar.markdown("""
**For best results, please include:**
- **Gender** (e.g., Male/Female/Other)
- **Age** (e.g., 45 years)
- **Symptoms** (e.g., chest pain, fever, cough)
- **Past Medical History** (e.g., diabetes, hypertension)
- **Family Health Background** (e.g., heart disease in family)
- **Other Relevant Details** (e.g., medications, allergies)
""")

# Language selection


st.title("🩺 MedNote AI - Health Risk Predictor")
st.write("Enter a detailed medical note or description below to predict risk level and receive a comprehensive explanation.")

user_input = st.text_area(
    "🧾 Doctor Note / Patient Description",
    placeholder="E.g., 57-year-old female with chest pain, irregular heartbeat, high blood pressure. Past history of hypertension. Family history of heart disease."
)
language = st.selectbox(
    "Select Explanation Language",
    ["English", "Hindi", "Spanish", "French", "German"]
)

if st.button("Predict & Describe"):
    if user_input.strip():
        label, score = predict_health_risk(user_input, vectorizer, clf_model, reg_model)
        st.success(f"**Predicted Risk Label:** {label}")
        st.info(f"**Predicted Risk Score:** {score}%")

        with st.spinner("Generating detailed medical explanation..."):
            description = generate_descriptive_answer(user_input, label, score, language=language)
        st.write("### 🩺 Detailed Medical Explanation:")
        description = "\n".join(line.strip() for line in description.splitlines() if line.strip())
        st.markdown(description, unsafe_allow_html=False)
    else:
        st.warning("Please enter a valid description including gender, age, symptoms, and relevant history.")
