import streamlit as st
import json
import random
import os

# Base directory
BASE_DIR = os.path.dirname(__file__)
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")

# Load questions
with open(QUESTIONS_FILE, "r") as f:
    questions = json.load(f)

# Shuffle questions
shuffled_questions = questions.copy()
random.shuffle(shuffled_questions)

st.title("Quiz Game 🎯")

# Initialize score
if "score" not in st.session_state:
    st.session_state.score = 0

# Loop through questions
for idx, q in enumerate(shuffled_questions):
    st.subheader(q["q"])
    options = q["options"]
    user_answer = st.radio("Choose an answer:", options, key=f"radio_{idx}")

    if st.button("Submit Answer", key=f"btn_{idx}"):
        if user_answer == q["a"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {q['a']}")
        st.write("---")

st.write(f"Your score: {st.session_state.score} / {len(shuffled_questions)}")