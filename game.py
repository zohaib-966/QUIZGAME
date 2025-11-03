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

st.title("Quiz Game 🎯")

# Initialize score
if "score" not in st.session_state:
    st.session_state.score = 0

# Initialize current question index
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

# Check if quiz is finished
if st.session_state.current_q >= len(st.session_state.shuffled_questions):
    st.success("🎉 Quiz Completed!")
    st.write(f"Your score: {st.session_state.score} / {len(st.session_state.shuffled_questions)}")
else:
    # Current question
    q = st.session_state.shuffled_questions[st.session_state.current_q]
    st.subheader(f"Question {st.session_state.current_q + 1}: {q['q']}")
    options = q["options"]

    # Radio button key
    radio_key = f"radio_{st.session_state.current_q}"

    # Reset radio selection for new question
    if radio_key not in st.session_state:
        st.session_state[radio_key] = None

    # Radio buttons
    user_answer = st.radio(
        "Choose an answer:",
        options,
        index=0 if st.session_state[radio_key] is None else options.index(st.session_state[radio_key]),
        key=radio_key
    )

    # Submit button
    if st.button("Submit Answer", key=f"btn_{st.session_state.current_q}"):
        st.session_state[radio_key] = user_answer  # save the selection

        if user_answer == q["a"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {q['a']}")

        # Move to next question
        st.session_state.current_q += 1
