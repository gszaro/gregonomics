from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from models import init_db, get_db, query_db
from debt_utils import snowball_strategy, avalanche_strategy

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize DB
init_db()

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_pw = generate_password_hash(password)

        db = get_db()
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
        db.commit()
        flash("Registered successfully. Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    transactions = query_db("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    debts = query_db("SELECT * FROM debts WHERE user_id = ?", (user_id,))
    return render_template("dashboard.html", transactions=transactions, debts=debts)

@app.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form["category"]
        note = request.form["note"]

        db = get_db()
        db.execute("INSERT INTO transactions (user_id, amount, category, note) VALUES (?, ?, ?, ?)",
                   (session["user_id"], amount, category, note))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_transaction.html")

@app.route("/debts", methods=["GET", "POST"])
def debts():
    if request.method == "POST":
        balance = float(request.form["balance"])
        interest = float(request.form["interest"])
        minimum = float(request.form["minimum"])

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
    raw_debts = query_db("SELECT balance, interest, minimum FROM debts WHERE user_id = ?", (user_id,))
    debts = [{"balance": d[0], "interest": d[1], "minimum": d[2]} for d in raw_debts]

    if not debts:
        flash("No debts found. Add some debts first.")
        return redirect(url_for("debts"))

    snowball = snowball_strategy([d.copy() for d in debts], extra_payment=100)
    avalanche = avalanche_strategy([d.copy() for d in debts], extra_payment=100)

    return render_template("simulate.html", snowball=snowball, avalanche=avalanche)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


