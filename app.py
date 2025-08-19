import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
from auth import register_user, login_user

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

# -------------------------------
# Safe Tweet Fetcher
# -------------------------------
def fetch_tweets(query, limit=50):
    tweets = []
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            tweets.append(tweet.content)
    except Exception as e:
        st.error(f"⚠️ Twitter scraping failed: {e}")
        return []
    return tweets


# -------------------------------
# Session state for login
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


# -------------------------------
# Login/Register UI
# -------------------------------
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

# -------------------------------
# Dashboard Page (After Login)
# -------------------------------
else:
    st.sidebar.success(f"Welcome {st.session_state.username} 👋")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📊 Real-Time Sentiment Analysis Dashboard")

    # Search box
    query = st.text_input("Enter keyword to search tweets (e.g. 'Python', 'AI', 'Modi')")
    limit = st.slider("Number of tweets", 10, 200, 50)

    if st.button("Analyze Sentiment"):
        analyzer = SentimentIntensityAnalyzer()
        tweets = fetch_tweets(query, limit)

        if not tweets:
            st.warning("No tweets found or scraping failed ❌")
        else:
            sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}

            # Sentiment classification
            tweet_sentiments = []
            for text in tweets:
                score = analyzer.polarity_scores(text)
                if score["compound"] > 0.05:
                    sentiments["Positive"] += 1
                    label = "Positive"
                elif score["compound"] < -0.05:
                    sentiments["Negative"] += 1
                    label = "Negative"
                else:
                    sentiments["Neutral"] += 1
                    label = "Neutral"
                tweet_sentiments.append({"Tweet": text, "Sentiment": label})

            df_counts = pd.DataFrame(list(sentiments.items()), columns=["Sentiment", "Count"])
            df_tweets = pd.DataFrame(tweet_sentiments)

            # -----------------------
            # Charts
            # -----------------------
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Sentiment Distribution")
                fig, ax = plt.subplots()
                sns.barplot(x="Sentiment", y="Count", data=df_counts, palette={"Positive": "green", "Negative": "red", "Neutral": "gray"}, ax=ax)
                st.pyplot(fig)

            with col2:
                st.subheader("🔄 Sentiment Share (%)")
                fig, ax = plt.subplots()
                ax.pie(df_counts["Count"], labels=df_counts["Sentiment"], autopct="%1.1f%%", colors=["green", "red", "gray"], startangle=90)
                st.pyplot(fig)

            # -----------------------
            # Tweets Table
            # -----------------------
            st.subheader("📌 Analyzed Tweets")
            st.dataframe(df_tweets.head(20), use_container_width=True)
