from PyPDF2 import PdfReader
import streamlit as st
import json

if "quiz" not in st.session_state:
    st.session_state.quiz = ""

if "score" not in st.session_state:
    st.session_state.score = 0

from ai_functions import (
    summarize_notes,
    simplify_notes,
    generate_quiz
)

st.title("SmartSem AI")

notes = ""

text_input = st.text_area("OR paste your notes here", height=200)

uploaded_file = st.file_uploader("Upload your notes (PDF)", type="pdf")

if text_input:
    notes = text_input

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            notes += text

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            notes += text

if st.button("Generate Summary"):

    if not notes.strip():
        st.warning("Please enter or upload notes first.")
    else:
        summary = summarize_notes(notes)
        st.subheader("Summary")
        st.write(summary)

if st.button("Simplify Notes"):

    simplified = simplify_notes(notes)

    st.subheader("Simplified Explanation")
    st.write(simplified)

difficulty = st.selectbox(
    "Select Quiz Difficulty",
    ["Easy", "Medium", "Hard"]
)

if st.button("Generate Quiz"):

    if not notes.strip():
        st.warning("Please upload or enter notes first.")
    else:
        st.session_state.quiz = generate_quiz(notes, difficulty)

if st.session_state.quiz:

    quiz_text = st.session_state.quiz.strip()

    if quiz_text.startswith("```json"):
        quiz_text = quiz_text.replace("```json", "", 1)

    if quiz_text.endswith("```"):
        quiz_text = quiz_text[:-3]

    try:
        quiz_data = json.loads(quiz_text)

    except json.JSONDecodeError:

        st.error("Failed to parse quiz data.")
        st.write("Raw response:")
        st.write(quiz_text)
        st.stop()

    user_answers = []

    for i, q in enumerate(quiz_data):

        st.subheader(f"Question {i+1}")

        answer = st.radio(
            q["question"],
            q["options"],
            key=f"q{i}"
        )

        user_answers.append(answer)

    if st.button("Submit Quiz"):

        score = 0

        for i, q in enumerate(quiz_data):
            if user_answers[i] == q["answer"]:
                score += 1

        st.success(
            f"Your Score: {score}/{len(quiz_data)}"
        )