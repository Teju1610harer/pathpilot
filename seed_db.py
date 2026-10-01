import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

with open("data/careers.json", "r", encoding="utf-8") as f:
    careers = json.load(f)

with open("data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

db.careers.delete_many({})
db.questions.delete_many({})

db.careers.insert_many(careers)
db.questions.insert_many(questions)

print(f"Inserted {len(careers)} careers.")
print(f"Inserted {len(questions)} questions.")