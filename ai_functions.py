import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ---------------- SUMMARY ----------------
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

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text


# ---------------- SIMPLIFY ----------------
def simplify_notes(notes):
    prompt = f"""
    Explain these notes in simple language suitable for beginners:

    {notes}
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text


# ---------------- QUIZ ----------------
def generate_quiz(notes, difficulty):
    prompt = f"""
    Create 5 {difficulty} multiple choice questions.

    Return ONLY a JSON array.

    Each question must include:
    - question
    - options (4 choices)
    - answer

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

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text
