# import praw

# reddit = praw.Reddit(
#     client_id="p3GEXrFNaClvkBnX-LK7FA",
#     client_secret="m5YkTfemvFDZNxyG9jhv-5WSKM7Azg",
#     user_agent="SentimentAnalysisBot/0.1 by u/Maleficent-Bank-1963"
# )

# for post in reddit.subreddit("python").hot(limit=5):
#     print(post.title)
# D:\Sentiment Analysis\reddit_client.py

import praw  # Reddit API wrapper

def get_reddit():
    """
    Returns a Reddit instance using PRAW.
    Credentials.
    """
    reddit = praw.Reddit(
        client_id="p3GEXrFNaClvkBnX-LK7FA",
        client_secret="m5YkTfemvFDZNxyG9jhv-5WSKM7Azg",
        user_agent="SentimentAnalysisBot/0.1 by u/Maleficent-Bank-1963"
    )
    return reddit

# Optional sanity check
if __name__ == "__main__":
    r = get_reddit()
    print("Reddit client initialized:", r.read_only)
