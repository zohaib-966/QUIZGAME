import streamlit as st
import random
import json
import os

st.set_page_config(page_title="Quiz App", page_icon="🧠")

st.title("🧠 Simple Quiz App")

# -------------------------------
# Load questions from JSON
# -------------------------------
if "questions_loaded" not in st.session_state:
    json_path = os.path.abspath("questions.json")
    st.write(f"📄 Loading questions from: `{json_path}`")

    with open("questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Validate questions
    valid_questions = []
    for i, q in enumerate(questions):
        if all(k in q for k in ["question", "options", "answer"]):
            valid_questions.append(q)
        else:
            st.warning(f"⚠️ Skipping question {i+1}: Missing keys {q}")

    random.shuffle(valid_questions)
    st.session_state.questions = valid_questions
    st.session_state.questions_loaded = True
    st.session_state.current_q = 0
    st.session_state.score = 0

# -------------------------------
# Quiz logic
# -------------------------------
if st.session_state.current_q < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current_q]

    st.subheader(f"Q{st.session_state.current_q + 1}: {q['question']}")

    radio_key = f"radio_{st.session_state.current_q}"
    user_answer = st.radio(
        "Choose an answer:",
        q["options"],
        key=radio_key
    )

    if st.button("Submit Answer"):
        if user_answer == q["answer"]:
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {q['answer']}")

        st.session_state.current_q += 1
        st.rerun()

else:
    st.success("🎉 Quiz Finished!")
    st.write(f"**Your final score:** {st.session_state.score} / {len(st.session_state.questions)}")

    if st.button("Restart Quiz"):
        random.shuffle(st.session_state.questions)
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.rerun()