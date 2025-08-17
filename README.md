📊 Gregonomics

A Personal Finance & Debt Manager with Simulations

🌐 Live Demo

#### Video Demo: <https://youtu.be/2aYQupSokN0)>

👉 Gregonomics on Render
(Click to try it live in your browser — no setup needed.)
https://gregonomics.onrender.com/

📖 Overview

Gregonomics is a full-stack web application that helps users take control of their financial journey. It provides tools to:

Track day-to-day transactions

Manage debts with balances, interest rates, and minimum payments

Simulate payoff strategies (Debt Snowball vs. Debt Avalanche) with interactive charts

Visualize progress toward financial freedom

Originally built as a CS50 capstone, Gregonomics is engineered with production-quality practices and clean UI/UX design.

✨ Features

🔐 User Authentication

Secure registration and login with hashed passwords (werkzeug.security)

Session-based authentication (Flask-Session)

💰 Transactions

Log income/expenses with categories and notes

Stored with timestamps, displayed in a Bootstrap-styled dashboard

📉 Debt Management

Add debts with balance, interest rate, and minimum payment

Persisted in SQLite3 with relational schema

📊 Debt Payoff Simulation

Snowball Method: Target smallest balances first (quick wins)

Avalanche Method: Target highest interest first (minimize interest)

Results rendered as interactive charts (Chart.js)

📋 Dashboard View

Unified display of transactions and debts

Quick actions to add entries and run simulations

🛠️ Tech Stack

Backend: Python 3, Flask, SQLite3

Frontend: HTML, Jinja2, Bootstrap 4, Chart.js

Auth: Flask-Session, Werkzeug password hashing

Deployment: Gunicorn + Render (easily portable to Heroku or any WSGI server)

⚙️ Installation & Setup (Local)

Clone the repo:

git clone https://github.com/YOUR_USERNAME/gregonomics.git
cd gregonomics

Create & activate a virtual environment:

python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

Install dependencies:

pip install -r requirements.txt

Initialize the database:

sqlite3 finance.db < schema.sql

Run the server:

python3 app.py

Then open: http://127.0.0.1:8080/

📐 Debt Algorithms

Snowball Method

Focus extra payments on the smallest balance first

Provides motivation with quick wins

Avalanche Method

Focus extra payments on highest interest rate

Minimizes total interest paid

Both simulate monthly progress until debts are cleared.

🚀 Usage

Register or log in to create your account

Add transactions to track income & expenses

Add debts with balances, rates, and minimums

Run a simulation → compare Snowball vs Avalanche payoff

View dashboard for a snapshot of financial health

🎯 Why This Project Matters

Gregonomics demonstrates:

Full-stack engineering with backend, database, and frontend integration

Real-world algorithms for financial decision-making

Production-ready practices: modular code, reusable templates, Bootstrap UI

A practical, usable app with immediate value

📜 License

MIT License
© 2025 Gregory Szaro
