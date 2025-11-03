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

# Initialize score and current question
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

st.title("Quiz Game 🎯")

# Check if there are more questions
if st.session_state.current_question < len(st.session_state.shuffled_questions):
    q = st.session_state.shuffled_questions[st.session_state.current_question]

    # Display question in a form
    with st.form(key=f"form_{st.session_state.current_question}"):
        st.subheader(q["q"])
        user_answer = st.radio("Choose an answer:", q["options"])
        submitted = st.form_submit_button("Submit Answer")

        if submitted:
            if user_answer == q["a"]:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {q['a']}")
            
            st.session_state.current_question += 1
            st.experimental_rerun()  # Move to next question

else:
    # Quiz finished
    st.write(f"Your score: {st.session_state.score} / {len(st.session_state.shuffled_questions)}")
    
    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_question = 0
        random.shuffle(st.session_state.shuffled_questions)
        st.experimental_rerun()