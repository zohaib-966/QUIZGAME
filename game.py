import streamlit as st
import json, random, os

# Base directory for JSON files
BASE_DIR = os.path.dirname(__file__)
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

# Load questions
with open(QUESTIONS_FILE, "r") as f:
    questions = json.load(f)

# Leaderboard functions
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Streamlit App
st.title("🎯 Quiz Game")

# Input player name
player_name = st.text_input("Enter your name:", "")

if st.button("Start Quiz") and player_name:
    score = 0
    shuffled_questions = questions.copy()
    random.shuffle(shuffled_questions)

    for q in shuffled_questions:
        st.subheader(q["question"])
        options = q["options"]
        user_answer = st.radio("Choose an answer:", options, key=q["question"])
        if st.button("Submit Answer", key=q["question"] + "_btn"):
            if user_answer == q["answer"]:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {q['answer']}")
            st.write("---")

    st.write(f"### 🎉 {player_name}, your final score: {score}/{len(shuffled_questions)}")

    # Update leaderboard
    leaderboard = load_leaderboard()
    leaderboard.append({"name": player_name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
    save_leaderboard(leaderboard)

# Show leaderboard
st.subheader("🏆 Leaderboard")
leaderboard = load_leaderboard()
for entry in leaderboard[:10]:
    st.write(f"{entry['name']} - {entry['score']}")