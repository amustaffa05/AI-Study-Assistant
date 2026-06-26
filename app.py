from PyPDF2 import PdfReader
import streamlit as st
import json
from ai_functions import (
    summarize_notes,
    simplify_notes,
    generate_quiz,
    answer_question
)

# ---------------- SESSION STATE ----------------
if "quiz" not in st.session_state:
    st.session_state.quiz = ""

st.title("LUNA GEMOK")

# ---------------- INPUT ----------------
notes = ""

text_input = st.text_area("paste your notes here", height=200)
uploaded_file = st.file_uploader("OR upload your notes (PDF)", type="pdf")

if text_input:
    notes = text_input

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            notes += text

# ---------------- SUMMARY ----------------
if st.button("Generate Summary"):
    if not notes.strip():
        st.warning("Please enter or upload notes first.")
    else:
        summary = summarize_notes(notes)
        st.subheader("Summary")
        st.write(summary)

# ---------------- SIMPLIFY ----------------
if st.button("Simplify Notes"):
    if not notes.strip():
        st.warning("Please enter or upload notes first.")
    else:
        simplified = simplify_notes(notes)
        st.subheader("Simplified Explanation")
        st.write(simplified)

# ----- after notes are ready (after PDF + text input) -----

st.subheader("Ask a Question")
user_question = st.text_input("Ask anything about your notes")

if st.button("Ask AI"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    elif not notes.strip():
        st.warning("Please upload or enter notes first.")
    else:
        answer = answer_question(notes, user_question)
        st.subheader("Answer")
        st.write(answer)

# ---------------- QUIZ ----------------
difficulty = st.selectbox(
    "Select Quiz Difficulty",
    ["Easy", "Medium", "Hard"]
)

if st.button("Generate Quiz"):
    if not notes.strip():
        st.warning("Please upload or enter notes first.")
    else:
        st.session_state.quiz = generate_quiz(notes, difficulty)

# ---------------- DISPLAY QUIZ ----------------
if st.session_state.quiz:

    quiz_text = st.session_state.quiz.strip()

    # remove markdown if AI adds it
    quiz_text = quiz_text.replace("```json", "").replace("```", "")

    try:
        quiz_data = json.loads(quiz_text)

    except json.JSONDecodeError:
        st.error("Quiz format error. Try again.")
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

        st.success(f"Your Score: {score}/{len(quiz_data)}")
