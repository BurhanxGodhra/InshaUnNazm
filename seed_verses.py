# seed_verses.py
from pymongo import MongoClient

client = MongoClient("mongodb+srv://nazm-admin:nazm1447@cluster0.wcfqdle.mongodb.net/poetry_platform")
db = client.poetry_platform
verses = [
    {"id": "1", "text": "Sample verse 1", "author": "Poet 1", "day": 1},
    {"id": "2", "text": "Sample verse 2", "author": "Poet 2", "day": 2}
]
db.opening_verses.insert_many(verses)
print("Inserted verses")

