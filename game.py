import streamlit as st
import random
import json

# -------------------------------
# Load questions from JSON
# -------------------------------
if "questions_loaded" not in st.session_state:
    with open("questions.json", "r") as f:
        st.session_state.questions = json.load(f)
    random.shuffle(st.session_state.questions)
    st.session_state.questions_loaded = True

# -------------------------------
# Initialize session state
# -------------------------------
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# -------------------------------
# Quiz logic
# -------------------------------
if st.session_state.current_q < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current_q]

    # Safety check
    if "question" not in q or "options" not in q or "answer" not in q:
        st.error("⚠️ JSON question missing keys!")
        st.stop()

    st.subheader(q["question"])

    # Unique key for each radio button
    radio_key = f"radio_{st.session_state.current_q}"
    if radio_key not in st.session_state:
        st.session_state[radio_key] = None

    user_answer = st.radio(
        "Choose an answer:",
        q["options"],
        index=0 if st.session_state[radio_key] is None else q["options"].index(st.session_state[radio_key]),
        key=radio_key
    )

    if st.button("Submit Answer"):
        st.session_state[radio_key] = user_answer
        if user_answer == q["answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {q['answer']}")

        st.session_state.current_q += 1
        st.experimental_rerun = lambda: None  # Safe dummy for Streamlit 1.51
        st.experimental_rerun = None

else:
    st.write("### 🎉 Quiz Finished!")
    st.write(f"Your final score: {st.session_state.score} / {len(st.session_state.questions)}")

    if st.button("Restart Quiz"):
        st.session_state.current_q = 0
        st.session_state.score = 0
        random.shuffle(st.session_state.questions)
        st.experimental_rerun = lambda: None
        st.experimental_rerun = None