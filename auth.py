import pymongo
from passlib.hash import bcrypt

# 🔗 MongoDB connection
# Encode @ as %40 in password
MONGO_URI = "mongodb+srv://ayushmishra180904:ayush%402004@cluster0.ljeo5h4.mongodb.net/?retryWrites=true&w=majority"

try:
    # Connect to MongoDB
    client = pymongo.MongoClient(MONGO_URI)
    db = client["sentimentDB"]   # use your DB here
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
    if user and bcrypt.verify(password, user["password"]):
        return True
    return False


if __name__ == "__main__":
    # Test block (run only manually)
    username = "ayush"
    password = "ayush@2004"

    registered = register_user(username, password)
    print("Registering user:", "Success ✅" if registered else "Already exists ⚠️")

    login_success = login_user(username, password)
    print("Login with correct password:", login_success)

    login_fail = login_user(username, "wrongpass")
    print("Login with wrong password:", login_fail)
