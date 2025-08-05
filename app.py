#!/usr/bin/env python
# coding: utf-8

# In[9]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import os
import nltk
import random
import calendar


# In[12]:


import streamlit as st

#Streamlit must start with this line
st.set_page_config(page_title="Mental Wellness Chatbot", layout="centered")

#CSS 
st.markdown('''
    <style>body {
        background-color: #121212;
        color: #FFFFFF;
    }

    .stApp {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 10px;
    }

    section[data-testid="stSidebar"] {
        background-color: #1A1A1A;
        color: #FFFFFF;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border-radius: 8px;
    }

    .stButton > button {
        background-color: #0072ff;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #005edc;
        transform: scale(1.05);
    }

    h1, h2, h3, p, label, .stMarkdown {
        color: #FFFFFF !important;
    }
div[data-baseweb="select"] > div {
    background-color: #2E2E2E !important;
    color: #FFFFFF !important;
    border: 1px solid #555 !important;
}
div[data-baseweb="select"] div[role="option"] {
    background-color: #1E1E1E;
    color: #FFFFFF;
}
</style>
''', unsafe_allow_html=True)
st.markdown("""
    <style>
    .stDownloadButton button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stDownloadButton button:hover {
        background-color: #0056b3;
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Mental Wellness Chatbot")
st.markdown("#### 🌟 *Your daily companion for mental well-being*")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import os
import nltk
import random

#Download VADER lexicon 
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

#File paths
MOOD_CSV = "mood_log.csv"
JOURNAL_FILE = "journal_entries.txt"
STREAK_FILE = "streaks.txt"

#Quotes and breathing tips for mood feedback
quotes = [
    "You're stronger than you think.",
    "Take a deep breath. You’re doing great.",
    "Every day is a fresh start.",
    "Keep going — better days are ahead."
]

breathing_tips = [
    "Try box breathing: Inhale 4s, hold 4s, exhale 4s, hold 4s.",
    "Close your eyes and take 5 deep breaths.",
    "Breathe in through your nose and exhale slowly through your mouth."
]

#Streamlit config
st.markdown("""
""", unsafe_allow_html=True)


#Sidebar menu
tab = st.sidebar.selectbox("Choose an option", [
    "Mood Check",
    "Journal",
    "Mood Chart",
    "Wellness Quiz",
    "Escape Room",
    "Achievements",
    "Mood Match Game",
    "Puzzle Game",
    "Journal Reminder",
    "Feedback",
    "Color Focus Game"  
])


#Streak and Badge Logic
def update_streak():
    today = datetime.now().date()
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, 'r') as f:
            last_date = f.readline().strip()
            streak = int(f.readline().strip())
        last_date = datetime.strptime(last_date, '%Y-%m-%d').date()
        if today == last_date:
            return streak, False
        elif today == last_date + pd.Timedelta(days=1):
            streak += 1
        else:
            streak = 1
    else:
        streak = 1
    with open(STREAK_FILE, 'w') as f:
        f.write(f"{today}\n{streak}")
    return streak, True

streak, new_day = update_streak()

#Mood Check
if tab == "Mood Check":
    st.header("💬 Mood Check-In")
    st.write(f"🔥 Current Streak: {streak} day(s)")
    if streak >= 3:
        st.success("🏅 Badge Unlocked: 3-Day Consistency Champion!")
    if streak >= 7:
        st.success("🥇 Badge Unlocked: 7-Day Wellness Streak!")

    user_input = st.text_input("How are you feeling today?")
    if user_input:
        sentiment = analyzer.polarity_scores(user_input)
        score = sentiment['compound']
        st.write(f"Sentiment Score: {round(score, 2)}")
        if score > 0.2:
            st.success("😊 Positive mood detected!")
            st.write(random.choice(quotes))
        elif score < -0.2:
            st.warning("😟 Low mood detected. Try this:")
            st.write(random.choice(breathing_tips))
        else:
            st.info("😐 Neutral mood. Here's something helpful:")
            st.write(random.choice(quotes + breathing_tips))

#Journal
elif tab == "Journal":
    st.header("📝 Journal Entry")
    entry = st.text_area("Write about your day...")
    
    if st.button("Save Journal Entry"):
        if entry.strip():
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            score = analyzer.polarity_scores(entry)['compound']
            sentiment = 'Positive 😊' if score >= 0.05 else 'Negative 😞' if score <= -0.05 else 'Neutral 😐'
            
            with open(JOURNAL_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{date}:\n{entry}\nSentiment: {sentiment}\n---\n")
            
            st.success(f"Journal saved. Sentiment: {sentiment}")
        else:
            st.warning("Please write something before saving.")

    st.subheader("📖 View Past Entries")
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, 'r', encoding='utf-8') as f:
            st.text(f.read())
    else:
        st.info("No journal entries yet.")
    if os.path.exists(JOURNAL_FILE):
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            journal_data = f.read()

        st.download_button(
            label="📥 Download Journal Entries",
            data=journal_data,
            file_name="journal_export.txt",
            mime="text/plain"
        )
    else:
        st.info("No journal entries available to download.")


#Mood Chart
elif tab == "Mood Chart":
    st.header("📈 Mood Trend Chart")
    if os.path.exists(MOOD_CSV):
        df = pd.read_csv(MOOD_CSV)
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)
        
        # Line Chart
        fig, ax = plt.subplots()
        ax.plot(df['date'], df['mood'], marker='o', linestyle='-')
        ax.set_title("Mood Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood (1–5)")
        ax.grid(True)
        fig.autofmt_xdate()  
        st.pyplot(fig)

        # Download Button
        with open(MOOD_CSV, 'r') as f:
            st.download_button(
                label="📥 Download Mood Log CSV",
                data=f.read(),
                file_name="mood_log.csv",
                mime="text/csv"
            )

        # Mood Calendar Heatmap
        st.subheader("🗓️ Mood Calendar Heatmap")

        # Prepare data for heatmap
        df['day'] = df['date'].dt.day
        df['weekday'] = df['date'].dt.weekday
        df['week'] = df['date'].dt.isocalendar().week
        df['month'] = df['date'].dt.month

        current_month = datetime.now().month
        calendar_df = df[df['month'] == current_month]

        if not calendar_df.empty:
            pivot = calendar_df.pivot_table(index='weekday', columns='day', values='mood')
            fig, ax = plt.subplots(figsize=(10, 3))
            sns.heatmap(pivot, cmap="coolwarm", linewidths=0.5, linecolor='gray', ax=ax, cbar=True)
            ax.set_yticklabels([calendar.day_name[i] for i in range(7)], rotation=0)
            ax.set_title("Mood Heatmap for Current Month")
            st.pyplot(fig)
        else:
            st.info("No mood entries for this month yet.")
    else:
        st.info("No mood data to display yet.")

# Mood Log Download
    with open(MOOD_CSV, 'r') as f:
        st.download_button(
            label="📥 Download Mood Log CSV",
            data=f.read(),
            file_name="mood_log.csv",
            mime="text/csv",
            key="download_mood_log_chart"  
        )

#Wellness Quiz
elif tab == "Wellness Quiz":
    st.header("🧪 Mental Wellness Self-Check")
    q1 = st.radio("1. How often do you feel overwhelmed?", ["Rarely", "Sometimes", "Often"], key="q1")
    q2 = st.radio("2. How well do you sleep at night?", ["Very well", "Okay", "Not well"], key="q2")
    q3 = st.radio("3. How supported do you feel by others?", ["Very supported", "Somewhat", "Not much"], key="q3")
    q4 = st.radio("4. Do you often feel anxious or restless?", ["No", "Sometimes", "Yes"], key="q4")
    if st.button("Get Recommendation"):
        score = 0
        if q1 == "Often": score += 1
        if q2 == "Not well": score += 1
        if q3 == "Not much": score += 1
        if q4 == "Yes": score += 1
        st.subheader("📝 Your Result:")
        if score <= 1:
            st.success("You're doing well! Keep taking care of yourself.")
        elif score == 2:
            st.info("You're under moderate stress. Try journaling or going for a walk.")
        else:
            st.warning("You're likely experiencing high stress. Try deep breathing or talk to someone you trust.")

#Escape Room
elif tab == "Escape Room":
    if "room" not in st.session_state:
        st.session_state.room = 1
    if "escaped" not in st.session_state:
        st.session_state.escaped = False
    if "room_unlocked" not in st.session_state:
        st.session_state.room_unlocked = False

    st.header("🔐 Mental Wellness Escape Room")

    #ROOM 1
    if st.session_state.room == 1:
        st.subheader("Room 1: The Anxious Chamber")
        st.write("You find yourself in a room filled with loud thoughts and racing worries.")
        ans1 = st.radio("What technique helps calm your breath using equal counts in and out?",
                        ["Power breathing", "Box breathing", "Fast inhaling"], key="ans1")
        if st.button("Submit Answer", key="sub1"):
            if ans1 == "Box breathing":
                st.success("Correct! You feel the noise in the room quiet down.")
                st.session_state.room_unlocked = True
            else:
                st.error("Not quite. Try again or rethink your approach.")

        if st.session_state.room_unlocked and st.button("Next Room"):
            st.session_state.room = 2
            st.session_state.room_unlocked = False
            st.rerun()

    #ROOM 2
    elif st.session_state.room == 2:
        st.subheader("Room 2: The Foggy Mirror")
        st.write("You see reflections of self-doubt and low energy.")
        ans2 = st.radio("Which of the following is a good practice for self-reflection?",
                        ["Multitasking", "Gratitude journaling", "Doomscrolling"], key="ans2")
        if st.button("Submit Answer", key="sub2"):
            if ans2 == "Gratitude journaling":
                st.success("Correct! The mirror clears, and you see a door ahead.")
                st.session_state.room_unlocked = True
            else:
                st.error("Not quite. Try again with intention.")

        if st.session_state.room_unlocked and st.button("Next Room"):
            st.session_state.room = 3
            st.session_state.room_unlocked = False
            st.rerun()

    #ROOM 3
    elif st.session_state.room == 3 and not st.session_state.escaped:
        st.subheader("Room 3: The Final Gate")
        st.write("You hear a voice: 'Your mind is powerful. But what empowers it the most?'")
        ans3 = st.radio("Pick the strongest wellness anchor:",
                        ["Avoiding emotions", "Social connection", "Perfectionism"], key="ans3")
        if st.button("Escape the Room", key="sub3"):
            if ans3 == "Social connection":
                st.balloons()
                st.success("You did it! You've escaped the mental maze and found balance. 🌟")
                st.session_state.escaped = True
            else:
                st.error("The gate remains closed. Reflect and try again.")

    #ESCAPED
    if st.session_state.escaped:
        st.info("Thanks for playing. Every right answer reflects something that helps your real wellness journey.")

  

#Achievements
#Achievements
elif tab == "Achievements":
    st.header("🏆 Your Achievements")
    st.write(f"🔥 Current Streak: {streak} day(s)")
    if streak >= 3:
        st.success("🏅 3-Day Consistency Champion")
    if streak >= 7:
        st.success("🥇 7-Day Wellness Streak")
    if streak < 3:
        st.info("Start journaling daily to unlock badges!")

    # ✅ Move it here
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, 'r') as f:
            st.download_button(
                label="📥 Download Streaks Log",
                data=f.read(),
                file_name="streaks.txt",
                mime="text/plain"
            )


#Mood Match Game
elif tab == "Mood Match Game":
    st.header("Mood Match Game")
    st.write("Match mood words with their corresponding emoji descriptions!")

    mood_pairs = {
        "Happy": "😊",
        "Sad": "😢",
        "Angry": "😡",
        "Relaxed": "😌",
        "Anxious": "😰",
        "Excited": "🤩"
    }

    if "mood_match_score" not in st.session_state:
        st.session_state.mood_match_score = 0
        st.session_state.shuffled_words = list(mood_pairs.keys())
        st.session_state.shuffled_emojis = list(mood_pairs.values())
        random.shuffle(st.session_state.shuffled_words)
        random.shuffle(st.session_state.shuffled_emojis)

    st.subheader("Match the Word with the Emoji")

    for i, word in enumerate(st.session_state.shuffled_words):
        emoji_guess = st.selectbox(f"What emoji matches '{word}'?", st.session_state.shuffled_emojis, key=f"emoji_{i}")
        if st.button(f"Submit Match for {word}", key=f"submit_{i}"):
            correct_emoji = mood_pairs[word]
            if emoji_guess == correct_emoji:
                st.success("✅ Correct!")
                st.session_state.mood_match_score += 1
            else:
                st.error(f"❌ Incorrect! The correct match for {word} is {correct_emoji}.")

    st.markdown(f"### 🏁 Your Score: `{st.session_state.mood_match_score}` / {len(mood_pairs)}")

    if st.button("🔄 Play Again"):
        st.session_state.mood_match_score = 0
        random.shuffle(st.session_state.shuffled_words)
        random.shuffle(st.session_state.shuffled_emojis)

#Puzzle Game
elif tab == "Puzzle Game":
    st.header("🧩 Word Unscramble Puzzle")
    st.write("Unscramble the letters to find a mental wellness word!")

    # Mental wellness themed words and their definitions
    word_bank = {
        "resilience": "The capacity to recover quickly from difficulties.",
        "mindfulness": "Being aware of the present moment.",
        "gratitude": "The quality of being thankful.",
        "breathe": "What you should do slowly when you're anxious.",
        "balance": "Mental steadiness and emotional stability."
    }

    # Initialize session state
    if "used_words" not in st.session_state:
        st.session_state.used_words = set()
    if "puzzle_score" not in st.session_state:
        st.session_state.puzzle_score = 0
    if "current_word" not in st.session_state or "new_word_requested" not in st.session_state:
        st.session_state.new_word_requested = True

    # Pick a new word if needed
    if st.session_state.new_word_requested:
        remaining_words = list(set(word_bank.keys()) - st.session_state.used_words)
        if not remaining_words:
            st.success("🎉 You've completed all puzzles!")
            if st.button("🔄 Restart Game"):
                st.session_state.used_words.clear()
                st.session_state.puzzle_score = 0
                st.session_state.new_word_requested = True
            st.stop()
        st.session_state.current_word = random.choice(remaining_words)
        st.session_state.shuffled_word = ''.join(random.sample(st.session_state.current_word, len(st.session_state.current_word)))
        st.session_state.guess_result = None
        st.session_state.new_word_requested = False

    st.markdown(f"### 🔤 Unscramble this: `{st.session_state.shuffled_word}`")
    guess = st.text_input("Your guess:")

    if st.button("Check Answer"):
        if guess.strip().lower() == st.session_state.current_word:
            st.session_state.guess_result = "correct"
            st.session_state.used_words.add(st.session_state.current_word)
            st.session_state.puzzle_score += 1
        else:
            st.session_state.guess_result = "wrong"

    if st.session_state.guess_result == "correct":
        st.success("🎉 Correct!")
        st.markdown(f"💡 *{st.session_state.current_word.title()}*: {word_bank[st.session_state.current_word]}")
        if st.button("Next Puzzle"):
            st.session_state.new_word_requested = True
            st.rerun()


    elif st.session_state.guess_result == "wrong":
        st.error("❌ Not quite. Try again!")

    st.markdown(f"### 🏆 Score: `{st.session_state.puzzle_score}`")

    
#Journal Reminder
elif tab == "Journal Reminder":
    st.header("📧 Email Journal Reminder")
    st.markdown("Set up a daily reminder to write in your journal.")
    st.info("💡 This uses Gmail. You must enable 2FA and create an App Password.")

    user_email = st.text_input("Enter your email address")

    sender_email = "sanatsunny10@gmail.com"  
    app_password = "spat lpvc eonh osyh"     

    if st.button("Send Reminder Now"):
        if user_email:
            try:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart

                subject = "📝 Don't forget your daily journal!"
                body = """
                Hi there,

                Just a gentle nudge to reflect on your day and write in your journal. 😊
                Journaling helps improve mental clarity and well-being.

                - Your Mental Wellness Chatbot
                """

                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = user_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, app_password)
                server.send_message(msg)
                server.quit()

                st.success("✅ Email reminder sent successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
        else:
            st.warning("Please enter an email address.")
# Feedback Tab
elif tab == "Feedback":
    st.header("💬 We value your feedback!")

    name = st.text_input("Your Name (optional):")
    rating = st.slider("How would you rate your experience?", 1, 5)
    comments = st.text_area("Any suggestions or thoughts?")

    if st.button("Submit Feedback"):
        if comments.strip():
            feedback_data = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{name},{rating},{comments}\n"
            with open("feedback.csv", "a", encoding="utf-8") as f:
                f.write(feedback_data)
            st.success("✅ Thank you for your feedback!")
        else:
            st.warning("Please add a comment before submitting.")
# Color Focus Game
elif tab == "Color Focus Game":
    st.header("🎨 Relaxation Color Focus Game")
    st.write("Choose a color you're drawn to. Each has a message for your well-being:")

    colors = {
        "💙 Blue": "Take a deep breath and let calmness wash over you.",
        "💚 Green": "You're grounded and connected to peace.",
        "💛 Yellow": "Happiness radiates from within. Let it shine!",
        "🧡 Orange": "You're full of creative energy and strength.",
        "💜 Purple": "Trust your intuition and inner wisdom.",
        "❤️ Red": "You are powerful and passionate. Honor your feelings."
    }

    selected_color = st.radio("Which color do you feel connected to today?", list(colors.keys()))
    
    if st.button("Reveal Message"):
        st.success(colors[selected_color])


# In[ ]:





# In[ ]:





# In[ ]:




