# Importing Flask and helpers so we can build a web app with pages, forms, and sessions
from flask import Flask, render_template, request, redirect, session, url_for, flash
# Flask-Session lets us keep user sessions stored on the server side (safer, scalable)
from flask_session import Session
# Werkzeug has built-in password hashing tools so we don’t store raw passwords (super important)
from werkzeug.security import generate_password_hash, check_password_hash
# Custom helpers from models.py to connect/query the database
from models import init_db, get_db, query_db
# Debt payoff strategies from our utils file
from debt_utils import snowball_strategy, avalanche_strategy

# Create a Flask app instance, point it to our templates and static folders
app = Flask(__name__, template_folder="templates", static_folder="static")

# Secret key is needed to use sessions securely
app.secret_key = "your_secret_key"
# Store sessions on the file system (instead of cookies only)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# On startup, set up the database tables from schema.sql
init_db()

@app.route("/")
def index():
    # If the user is already logged in, send them straight to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    # Otherwise, show them the landing page (index.html)
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # If user submits the form (POST), we process registration
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Hash the password before saving to DB (never store plain text!)
        hash_pw = generate_password_hash(password)

        db = get_db()
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
        db.commit()
        flash("Registered successfully. Please log in.")  # Friendly message to user
        return redirect(url_for("login"))
    # If GET, just show the register.html form
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Look for this user in the DB
        user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)

        # If user exists and password matches the hashed one in DB, log them in
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]  # store their id in session
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Clear the session to log out
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    # Get all this user’s transactions and debts
    transactions = query_db("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    debts = query_db("SELECT * FROM debts WHERE user_id = ?", (user_id,))
    return render_template("dashboard.html", transactions=transactions, debts=debts)

@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        # Grab form data
        amount = float(request.form["amount"])
        category = request.form["category"]
        note = request.form["note"]

        # Insert into database
        db = get_db()
        db.execute("INSERT INTO transactions (user_id, amount, category, note) VALUES (?, ?, ?, ?)",
                   (session["user_id"], amount, category, note))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_transaction.html")

@app.route("/debts", methods=["GET", "POST"])
def debts():
    if request.method == "POST":
        # New debt info entered by user
        balance = float(request.form["balance"])
        interest = float(request.form["interest"])
        minimum = float(request.form["minimum"])

        # Save to DB
        db = get_db()
        db.execute("INSERT INTO debts (user_id, balance, interest, minimum) VALUES (?, ?, ?, ?)",
                   (session["user_id"], balance, interest, minimum))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("debts.html")

@app.route("/simulate")
def simulate():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    # Pull debts for this user
    raw_debts = query_db("SELECT balance, interest, minimum FROM debts WHERE user_id = ?", (user_id,))
    debts = [{"balance": d[0], "interest": d[1], "minimum": d[2]} for d in raw_debts]

    if not debts:
        flash("No debts found. Add some debts first.")
        return redirect(url_for("debts"))

    # Run both strategies side by side with an extra $100 payment
    snowball = snowball_strategy([d.copy() for d in debts], extra_payment=100)
    avalanche = avalanche_strategy([d.copy() for d in debts], extra_payment=100)

    return render_template("simulate.html", snowball=snowball, avalanche=avalanche)

if __name__ == "__main__":
    # Start the web server on port 8080, debug=True auto-reloads on code changes
    app.run(host="0.0.0.0", port=8080, debug=True)
