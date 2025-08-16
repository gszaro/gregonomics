############################################################

# ClearPay

# A Personal Finance & Debt Manager with Simulations

############################################################

## Overview

ClearPay is a full-stack web application that helps users take control of their financial journey. It provides tools to:

- Track day-to-day transactions
- Manage debts with balances, interest rates, and minimum payments
- Simulate payoff strategies (Debt Snowball vs. Debt Avalanche) with interactive charts
- Visualize progress toward financial freedom

This project was built as a capstone to CS50, but engineered to showcase production-quality software practices and thoughtful design.

---

## Features

- User Authentication

  - Secure registration and login using hashed passwords (werkzeug.security)
  - Session-based authentication (Flask-Session)

- Transactions

  - Log income or expenses with categories and notes
  - Timestamped and displayed in a clean, Bootstrap-styled dashboard

- Debt Management

  - Add debts with balance, interest rate, and minimum payment
  - Store securely in SQLite3 with proper relational schema

- Debt Payoff Simulation

  - Snowball Method: Target smallest balances first
  - Avalanche Method: Target highest interest rates first
  - Results rendered as interactive line charts via Chart.js

- Dashboard View
  - Unified display of transactions and debts
  - Quick actions to add transactions, add debts, and run simulations

---

## Tech Stack

- Backend: Python 3, Flask, SQLite3
- Frontend: HTML, Jinja2, Bootstrap 4, Chart.js
- Authentication: Flask-Session, Werkzeug password hashing
- Deployment Ready: Lightweight and portable (Render, Heroku, or any WSGI server)

############################################################

# Installation and Setup

############################################################

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/clearpay.git
cd clearpay

Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
Install dependencies

pip install -r requirements.txt
Initialize the database

sqlite3 finance.db < schema.sql
Run the server

python3 app.py
By default: http://127.0.0.1:5000

############################################################
Debt Algorithms
############################################################

Snowball Method
Focus extra payments on the smallest balance.
Provides motivation with quick wins.

Avalanche Method
Focus extra payments on the highest interest rate.
Minimizes total interest paid over time.

Both algorithms iterate monthly, applying interest, payments, and recording balances until all debts are cleared.

############################################################
Usage
############################################################

Register or log in to create your secure account

Add transactions to track income and expenses

Add debts with balances, interest rates, and minimums

Run a simulation to compare Snowball vs Avalanche payoff trajectories

View the dashboard to monitor financial health at a glance

############################################################
Why This Project Matters
############################################################

ClearPay demonstrates:

Full-stack engineering with database, backend, and frontend integration

Applied algorithms for real-world financial decision making

Production-quality practices such as modular code, reusable templates, and Bootstrap UI

Strong portfolio showcase: a practical tool with immediate real-world value

Clearpay is a personal finance companion that could scale into a deployable product.

############################################################

# License

############################################################

MIT License  
Copyright (c) 2025 Gregory Szaro
