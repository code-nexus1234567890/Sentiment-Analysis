import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from auth import register_user, login_user
from reddit_client import get_reddit

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

# -------------------------------
# MongoDB setup
# -------------------------------
mongo_client = MongoClient(
    "mongodb+srv://ayushmishra180904:ayush2004@cluster0.ljeo5h4.mongodb.net/?retryWrites=true&w=majority"
)
db = mongo_client["sentimentDB"]
posts_collection = db["reddit_posts"]

# -------------------------------
# Reddit API setup
# -------------------------------
try:
    reddit = get_reddit()
except Exception as e:
    st.error(f"⚠️ Failed to initialize Reddit client: {e}")
    reddit = None


# -------------------------------
# Function: Fetch Reddit posts (SEARCH MODE)
# -------------------------------
def fetch_reddit_posts(query, limit=50):
    posts_list = []

    if reddit is None:
        st.error("Reddit client not initialized ❌")
        return posts_list

    try:
        # Search Reddit across all subreddits
        for post in reddit.subreddit("all").search(query, limit=limit):
            posts_list.append(post.title)
            post_data = {
                "id": post.id,
                "title": post.title,
                "author": str(post.author),
                "created_utc": post.created_utc,
                "score": post.score,
                "num_comments": post.num_comments,
                "url": post.url,
                "selftext": post.selftext,
            }
            posts_collection.insert_one(post_data)

        if not posts_list:
            st.warning("No posts found for this search term ❌")

    except Exception as e:
        st.error(f"⚠️ Error fetching Reddit posts: {e}")

    return posts_list


# -------------------------------
# Session state
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
# Dashboard Page
# -------------------------------
else:
    st.sidebar.success(f"Welcome {st.session_state.username} 👋")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📊 Real-Time Sentiment Analysis Dashboard")

    # Inputs
    query = st.text_input("Enter a topic or keyword (e.g., 'Virat Kohli', 'AI', 'Cricket')")
    limit = st.slider("Number of posts", 10, 200, 50)

    if st.button("Analyze Sentiment"):
        if not query.strip():
            st.warning("Please enter a keyword ❌")
        else:
            analyzer = SentimentIntensityAnalyzer()
            posts = fetch_reddit_posts(query, limit)

            if not posts:
                st.warning("No posts found or fetching failed ❌")
            else:
                # Sentiment classification
                sentiments = {"Positive": 0, "Negative": 0, "Neutral": 0}
                post_sentiments = []

                for text in posts:
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
                    post_sentiments.append({"Post": text, "Sentiment": label})

                # DataFrames
                df_counts = pd.DataFrame(list(sentiments.items()), columns=["Sentiment", "Count"])
                df_posts = pd.DataFrame(post_sentiments)

                # -----------------------
                # Charts
                # -----------------------
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📊 Sentiment Distribution")
                    fig, ax = plt.subplots()
                    sns.barplot(
                        x="Sentiment",
                        y="Count",
                        data=df_counts,
                        palette={"Positive": "green", "Negative": "red", "Neutral": "gray"},
                        ax=ax
                    )
                    st.pyplot(fig)

                with col2:
                    st.subheader("🔄 Sentiment Share (%)")
                    fig, ax = plt.subplots()
                    ax.pie(
                        df_counts["Count"],
                        labels=df_counts["Sentiment"],
                        autopct="%1.1f%%",
                        colors=["green", "red", "gray"],
                        startangle=90
                    )
                    st.pyplot(fig)

                # -----------------------
                # Posts Table
                # -----------------------
                st.subheader("📌 Analyzed  Posts")
                st.dataframe(df_posts.head(29), use_container_width=True)
