from flask import Blueprint, render_template, request
import hashlib
from .db import get_db

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        password_md5 = hashlib.md5(password.encode("utf-8")).hexdigest()

        db = get_db()
        user = db.execute(
            "SELECT id, username, role FROM users WHERE username = ? AND password_md5 = ?",
            (username, password_md5)
        ).fetchone()

        if user:
            return f"Connecté ✅ (id={user['id']}, username={user['username']}, role={user['role']})"
        else:
            return "Échec login ❌"

    return render_template("login.html")
