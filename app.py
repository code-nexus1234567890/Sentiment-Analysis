import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
from auth import register_user, login_user

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Login/Register UI
if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Menu", ["Login", "Register"])
    st.title("🔐 Sentiment Dashboard Login")

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

    elif choice == "Register":
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(username, password):
                st.success("Account created 🎉, please login.")
            else:
                st.error("Username already exists ❌")

else:
    st.sidebar.success(f"Welcome {st.session_state.username} 👋")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    st.title("📊 Real-Time Sentiment Analysis Dashboard")

    # Search box
    query = st.text_input("Enter keyword to search tweets")
    limit = st.slider("Number of tweets", 10, 200, 50)

    if st.button("Analyze Sentiment"):
        analyzer = SentimentIntensityAnalyzer()
        tweets = []
        sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            score = analyzer.polarity_scores(tweet.content)
            if score["compound"] > 0.05:
                sentiments["Positive"] += 1
            elif score["compound"] < -0.05:
                sentiments["Negative"] += 1
            else:
                sentiments["Neutral"] += 1
            tweets.append(tweet.content)

        df = pd.DataFrame(list(sentiments.items()), columns=["Sentiment", "Count"])

        # Show bar chart
        fig, ax = plt.subplots()
        ax.bar(df["Sentiment"], df["Count"], color=["green", "red", "gray"])
        st.pyplot(fig)

        # Show tweets
        st.subheader("📌 Sample Tweets")
        for t in tweets[:10]:
            st.write("-", t)
