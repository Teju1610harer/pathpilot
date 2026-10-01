import os
from features import compute_features
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["name"] = user["name"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
    return render_template("dashboard.html", name=session["name"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
@app.route("/assessment", methods=["GET", "POST"])
def assessment():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    if request.method == "POST":
        answers = {}
        for key in request.form:
            answers[key] = request.form.get(key)

        db.assessments.insert_one({
            "user_id": session["user_id"],
            "answers": answers
        })

        flash("Assessment submitted successfully!")
        return redirect(url_for("dashboard"))

    questions = list(db.questions.find({}, {"_id": 0}))
    return render_template("assessment.html", questions=questions)


@app.route("/features-test")
def features_test():
    if "user_id" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))

    latest = db.assessments.find_one(
        {"user_id": session["user_id"]},
        sort=[("_id", -1)]
    )
    if not latest:
        return "No assessment found. Take the assessment first."

    questions = list(db.questions.find({}, {"_id": 0}))
    result = compute_features(latest["answers"], questions)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

