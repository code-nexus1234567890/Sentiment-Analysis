import tweepy

# ======================
# 🔑 Add your credentials here
# ======================
bearer_token = "AAAAAAAAAAAAAAAAAAAAADuh3gEAAAAAeztLRWzvjnfxWcYn4JGTty%2BBTfI%3DjGbz2dm9mA1sQ2Qz3pfhtQ3ci8VJVJZ8ub4wHPuuPn7KRIDX89"   # paste your real bearer token here

# Initialize client
client = tweepy.Client(bearer_token=bearer_token)

# Function to fetch tweets
def get_tweets(query, max_results=10):
    """
    Fetches recent tweets based on a query.
    query: keyword or hashtag (e.g., "love", "#AI")
    max_results: number of tweets (max 100 per request)
    """
    try:
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=["id", "text", "created_at", "lang"],
            max_results=max_results
        )
        tweets = []
        if response.data:
            for tweet in response.data:
                tweets.append({
                    "time": tweet.created_at,
                    "text": tweet.text
                })
        return tweets
    except Exception as e:
        return [{"error": str(e)}]
