import os
from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=3000)
db = client[os.getenv("DB_NAME")]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    client.admin.command("ping")
    db.test.insert_one({"msg": "hello"})
    return jsonify(status="ok", db=db.name)

if __name__ == "__main__":
    app.run(debug=True)