import sys
sys.stdout.reconfigure(encoding='utf-8')
import pymongo
from passlib.hash import bcrypt

# -------------------------------
# 🔗 MongoDB Atlas connection
# -------------------------------
MONGO_URI = "mongodb+srv://2k23it2a2310456_db_user:rUkqPZKhNTNDYE5T@sentimentanalysis.4yl8yfe.mongodb.net/SentimentAnalysis?retryWrites=true&w=majority&appName=SentimentAnalysis"

try:
    # Connect to MongoDB Atlas
    client = pymongo.MongoClient(MONGO_URI)
    db = client["SentimentAnalysis"]   # Database name on Atlas
    users_collection = db["users"]     # Collection name
    print("✅ Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("❌ MongoDB Atlas connection failed:", e)


# -------------------------------
# 👤 Register user
# -------------------------------
def register_user(username, password):
    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return False
    
    # Hash the password
    hashed = bcrypt.hash(password)
    users_collection.insert_one({"username": username, "password": hashed})
    return True


# -------------------------------
# 🔐 Verify login
# -------------------------------
def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.verify(password, user["password"]):
        return True
    return False


# -------------------------------
# 🧪 Test Block
# -------------------------------
if __name__ == "__main__":
    username = "ayush"
    password = "ayush2004"

    registered = register_user(username, password)
    print("Registering user:", "Success ✅" if registered else "Already exists ⚠️")

    login_success = login_user(username, password)
    print("Login with correct password:", login_success)

    login_fail = login_user(username, "wrongpass")
    print("Login with wrong password:", login_fail)

