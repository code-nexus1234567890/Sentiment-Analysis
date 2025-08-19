import pymongo
from passlib.hash import bcrypt

# 🔗 MongoDB connection
MONGO_URI = "mongodb+srv://ayushmishra180904:ayush%402004@cluster0.ljeo5h4.mongodb.net/sentimentDB?retryWrites=true&w=majority"
client = pymongo.MongoClient(MONGO_URI)
db = client["sentimentDB"]
users_collection = db["users"]

# Register user
def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return False
    hashed = bcrypt.hash(password)
    users_collection.insert_one({"username": username, "password": hashed})
    return True

# Verify login
def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and bcrypt.verify(password, user["password"]):
        return True
    return False
