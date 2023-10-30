from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

db = SQL("sqlite:///project.db")


def register_user():
    # Get user input
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    if len(username) < 1 or len(password) < 1 or len(confirmation) < 1:
        return render_template("error.html", error="Not All Areas Are Filled")

    # Check if password and confirmation match
    if password != confirmation:
        return render_template("error.html", error="Password and Confirmation Do Not Match")

    # Check if user exists
    users = db.execute("SELECT username FROM users")
    for user in users:
        if user["username"] == username:
            return render_template("error.html", error="Username Already Exists")

    # Insert into database
    hash = generate_password_hash(password)
    db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
    return render_template("login.html")


def login_user():
    # Ensure username was submitted
    if not request.form.get("username"):
        return render_template("error.html", error="Must Provide Username")

    # Ensure password was submitted
    elif not request.form.get("password"):
        return render_template("error.html", error="Must Provide Password")

    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?",
                      request.form.get("username"))

    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        return render_template("error.html", error="Invalid Username and/or Password")

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return redirect("/")


def logout_user():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
