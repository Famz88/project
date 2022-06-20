import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///app.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    transactions_db = db.execute("SELECT symbol, name, SUM(shares) AS shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    total = cash
    for stock in transactions_db:
        total += stock["price"] * stock["shares"]

    return render_template("index.html", database = transactions_db, cash = usd(cash), total=usd(total), usd=usd)


# Allow user to change password
@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
    """Allow user to change their password"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("changepassword.html")

    # User reached route via POST (as by submitting a form via POST)
    current_pw = request.form.get("current_password")
    new_pw = request.form.get("new_password")
    confirm_new_pw = request.form.get("confirm_new_password")

    # Check whether the input box for current password is empty or not
    if not current_pw:
        return apology("You should input your current password")

    # Check whether the current password is correct or not
    old_password = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
    if len(old_password) != 1 or not check_password_hash(old_password[0]["hash"], current_pw):
        return apology("invalid username and/or password", 403)

    # New password and Confirm New Password Validation
    if not new_pw:
        return apology("You should input your new password")
    elif not confirm_new_pw:
        return apology("You should input your password in 'Confirmation New Password'")
    elif new_pw != confirm_new_pw:
        return apology("Password does not match")

    # Update the the new password for that user in database
    hashed_new_pw = generate_password_hash(new_pw)
    db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_new_pw, session["user_id"])

    # Redirect the user to login form
    return redirect("/logout")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = :id", id=user_id)
    return render_template("history.html", transactions = transactions_db)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST (as by submitting a form via POST)
    stock_info = lookup(request.form.get("symbol"))
    if not stock_info:
        return apology("Invalid symbol or This symbol does not exist")

    return render_template("quoted.html", name=stock_info["name"], price=usd(stock_info["price"]),
                           symbol=stock_info["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must Give Username")

        if not password:
            return apology("Must Give Password")

        if not confirmation:
            return apology("Must Give Confirmation")

        if password != confirmation:
            return apology("Passwords Do Not Much")

        hash = generate_password_hash(password)

        # Insert the user input in to database
        try:
           new_user = db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, hash)
        except:
            return apology("Username already exists")

        session["user_id"] = new_user

        return redirect("/")
