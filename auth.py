import sys
sys.stdout.reconfigure(encoding='utf-8')
import pymongo
import bcrypt   # native bcrypt, not passlib

# -------------------------------
# 🔗 MongoDB Atlas connection
# -------------------------------
MONGO_URI = "mongodb+srv://2k23it2a2310456_db_user:rUkqPZKhNTNDYE5T@sentimentanalysis.4yl8yfe.mongodb.net/SentimentAnalysis?retryWrites=true&w=majority&appName=SentimentAnalysis"

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["SentimentAnalysis"]
    Users_collection = db["Users"]
    print("✅ Connected to MongoDB Atlas successfully!")
except Exception as e:
    print("❌ MongoDB Atlas connection failed:", e)


# -------------------------------
# 👤 Register user
# -------------------------------
def register_user(username, password):
    # Check if username already exists
    if Users_collection.find_one({"username": username}):
        return False

    # Hash the password using bcrypt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    Users_collection.insert_one({
        "username": username,
        "password": hashed.decode("utf-8")  # store as string
    })
    return True


# -------------------------------
# 🔐 Verify login
# -------------------------------
def login_user(username, password):
    user = Users_collection.find_one({"username": username})
    if not user:
        return False

    stored_hash = user["password"].encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), stored_hash)


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
