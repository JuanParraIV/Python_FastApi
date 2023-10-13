from pymongo import MongoClient

# Base de datos Remota
db_client = MongoClient(
  "mongodb+srv://test:test@cluster0.a5escgu.mongodb.net/?retryWrites=true&w=majority"
).test
