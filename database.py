from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://admin:admin@cluster0.sctzjpt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["todo_db"]
todos_collection = db["todos"]
users_collection = db["users"]