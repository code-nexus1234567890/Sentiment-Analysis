import pymongo
from passlib.hash import bcrypt

# 🔗 MongoDB connection (no special chars now)
MONGO_URI = "mongodb+srv://ayushmishra18904_db_user:C1HS4K825qSAJQNe@cluster0.chp9js4.mongodb.net/sentimentDB?retryWrites=true&w=majority&appName=Cluster0"
# MONGO_URI = "mongodb+srv://ayushmishra18904_db_user:<db_password>@cluster0.chp9js4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    # Connect to MongoDB
    client = pymongo.MongoClient(MONGO_URI)
    db = client["sentimentDB"]   # Database name
    users_collection = db["users"]
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)


# Register user
def register_user(username, password):
    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return False
    
    # Hash password before saving
    hashed = bcrypt.hash(password)
    users_collection.insert_one({"username": username, "password": hashed})
    return True


# Verify login
def login_user(username, password):
    # Find user by username
    user = users_collection.find_one({"username": username})
    if not user:
        return False

    try:
        if bcrypt.verify(password, user["password"]):
            return True
    except ValueError:
        print("⚠️ Invalid password hash found in database for user:", username)
        return False

    return False


if __name__ == "__main__":
    # Test block
    username = "ayush"
    password = "ayush2004"

    registered = register_user(username, password)
    print("Registering user:", "Success ✅" if registered else "Already exists ⚠️")

    login_success = login_user(username, password)
    print("Login with correct password:", login_success)

    login_fail = login_user(username, "wrongpass")
    print("Login with wrong password:", login_fail)
