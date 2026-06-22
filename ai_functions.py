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
    You are an expert tutor.

    Create 5 {difficulty} multiple choice questions.

    Focus on testing understanding of the concepts.

    Rules:
    - Use simple student-friendly language.
    - Do NOT focus on difficult vocabulary.
    - Do NOT ask questions that only test word definitions.
    - Test comprehension and understanding of the notes.
    - Each question must have 4 answer choices.
    - Only one answer should be correct.

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

# ------- QnA Section --------
def answer_question(notes, question):
    prompt = f"""
    You are a helpful tutor.

    Use the notes below to answer the student's question.

    Notes:
    {notes}

    Question:
    {question}

    Rules:
    - Give clear and simple explanation
    - If possible, use examples
    - Keep it beginner friendly
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output_text
