import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=3000)
db = client[os.getenv("DB_NAME")]
users = db.users

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    client.admin.command("ping")
    return jsonify(status="ok", db=db.name)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if users.find_one({"email": email}):
            flash("Email already registered. Please login.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "student"
        })
        flash("Registration successful! You can now log in.")
        return redirect(url_for("register"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)