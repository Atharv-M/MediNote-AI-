from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.7,        # controls creativity
    api_key=api_key
)
# print(llm.invoke("what is the capital of india"))

prompt_template = """
Patient's symptoms: "{note}"
Predicted risk label: {risk_label}
Predicted risk score: {risk_score}%

Provide a short and concise medical explanation, including possible causes, severity, and recommended actions.
"""

chat_prompt = ChatPromptTemplate.from_template(prompt_template)


def generate_descriptive_answer(note, risk_label, risk_score):
    """
    Generate descriptive explanation using LangChain + Gemini
    """
    prompt = chat_prompt.format(
        note=note,
        risk_label=risk_label,
        risk_score=risk_score
    )
    response = llm.invoke(prompt)
    # If response is a dict, get the 'content' field
    
    
    return response.content.strip() # fallback if response is already a string

