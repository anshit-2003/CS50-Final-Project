import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from cryptography.fernet import Fernet
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Encryption For Password Manager
key = b'DCnnYi1vt1A3QxkMaa5lG17WHGMGjOvtfhdm_e2pBMU='
fernet = Fernet(key)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
@login_required
def main():
    return render_template("home.html")


@app.route("/index")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    tasks = db.execute("SElECT * FROM tasks WHERE user_id = ?", user_id)
    return render_template("index.html",tasks = tasks)


@app.route("/clipboard", methods=["GET","POST"])
@login_required
def Clipboard():
    """Show Calendar"""
    if request.method == "GET":
        return render_template("clipboard.html")


    user_id = session["user_id"]
    note = request.form.get("note")
    title = request.form.get("title")

    db.execute("INSERT INTO clipboard (user_id,note,date_added,title) VALUES(?,?,?,?)",user_id,note,datetime.datetime.now(),title)
    flash("Note Added!")
    return redirect("/clipboard")




@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    """Get List of all the tasks"""
    if request.method == "GET":
        return render_template("tasks.html")

    user_id = session["user_id"]
    task = request.form.get("task")
    deadline = request.form.get("deadline")
    db.execute("INSERT INTO tasks (user_id,task,deadline,completed) VALUES(?,?,?,?)",user_id,task,deadline,0)
    flash("Task Added Successfully!!")
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_pass = request.form.get("confirmation")
        if not username:
            return apology("A username Must be Provided")
        if not password:
            return apology("A Password Must be Provided")
        if not confirm_pass:
            return apology("A Confirmation Password Must be Provided")
        if password != confirm_pass:
            return apology("Different Passwords Entered")
        else:
            hash = generate_password_hash(password)
            try:
                db.execute("INSERT INTO users (username,hash) VALUES(?,?);", username, hash)
                return redirect("/login")
            except:
                return apology("Username Already Exists")



@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "GET":
        return render_template("change_password.html")

    password = request.form.get("password")
    confirm_pass = request.form.get("confirm_password")

    if (password != confirm_pass):
        return apology("Passwords Do Not Match!")

    hash = generate_password_hash(password)
    user_id = session["user_id"]
    db.execute("UPDATE users SET hash = ? WHERE id=?", hash, user_id)
    flash("Password Changed!")
    return redirect("/login")



@app.route("/notes",methods=["GET","POST"])
@login_required
def notes():
    user_id = session["user_id"]
    notes = db.execute("SELECT * FROM clipboard WHERE user_id=?",user_id)
    return render_template("notes.html",notes = notes)



@app.route("/password_manager",methods=["GET","POST"])
@login_required
def manager():
    if request.method == "GET":
        return render_template("password_manager.html")

    user_id = session["user_id"]
    master = request.form.get("master")
    rows = db.execute("SELECT hash FROM users WHERE id=?",user_id)
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], master):
        return apology("Wrong Master Password!")

    passwords = db.execute("SELECT * FROM passwords WHERE user_id=?",user_id)
    real_pass = {}
    for row in passwords:
        pass1 = fernet.decrypt(row["password"]).decode()
        real_pass[row["title"]] = pass1

    print(real_pass)
    return render_template("passwords.html",real_pass=real_pass)

@app.route("/add_pass",methods=["GET","POST"])
@login_required
def add_pass():
    if request.method == "GET":
        return render_template("add_pass.html")


    user_id = session["user_id"]
    title = request.form.get("title")
    new_password = request.form.get("password")
    encpass = fernet.encrypt(new_password.encode())
    db.execute("INSERT INTO passwords (user_id,password,title,date) VALUES(?,?,?,?)",user_id,encpass,title,datetime.datetime.now())
    flash("Password Added!")
    return redirect("/password_manager")


