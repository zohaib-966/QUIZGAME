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

# Shuffle questions once
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = questions.copy()
    random.shuffle(st.session_state.shuffled_questions)

# Initialize quiz state
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

st.title("Quiz Game 🎯")

# Current question index
idx = st.session_state.current_q

if idx < len(st.session_state.shuffled_questions):
    q = st.session_state.shuffled_questions[idx]
    st.subheader(f"Question {idx + 1}: {q['q']}")
    
    # Unique key for radio button
    radio_key = f"q_{idx}"
    user_answer = st.radio("Choose an answer:", q["options"], key=radio_key)

    # Submit button
    submit_key = f"submit_{idx}"
    if st.button("Submit Answer", key=submit_key):
        if user_answer == q["a"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {q['a']}")
        
        # Move to next question
        st.session_state.current_q += 1
        st.experimental_rerun()
else:
    st.write("### Quiz Finished!")
    st.write(f"Your final score: {st.session_state.score} / {len(st.session_state.shuffled_questions)}")

    # Optional: Restart button
    if st.button("Restart Quiz"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        random.shuffle(st.session_state.shuffled_questions)
        st.experimental_rerun()