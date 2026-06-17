import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    "gemini-3.5-flash",
    generation_config={"temperature": 0.7}
)

def summarize_notes(notes):
    prompt = f"""
    You are an expert tutor.

    Summarize the following notes into:
    - Key bullet points
    - Simple language
    - Important concepts only

    Notes:
    {notes}
    """

    response = model.generate_content(prompt)

    if response and response.text:
        return response.text
    else:
        return "No response generated. Please try again."


def simplify_notes(notes):
    prompt = f"""
    Explain these notes in simple language suitable for beginners:

    {notes}
    """

    response = model.generate_content(prompt)
    return response.text


def generate_quiz(notes, difficulty):
    prompt = f"""
    Create 5 {difficulty} multiple choice questions.

    Return ONLY a JSON array.

    Do not include:
    - explanations
    - markdown
    - code fences
    - ```json

    Example:

    [
      {{
        "question": "What is AI?",
        "options": [
          "Artificial Intelligence",
          "Automatic Internet",
          "Advanced Interface",
          "None"
        ],
        "answer": "Artificial Intelligence"
      }}
    ]

    Notes:
    {notes}
    """

    response = model.generate_content(prompt)
    return response.text