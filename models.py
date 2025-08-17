import sqlite3
from flask import g  # g is a special global object for current request context

DATABASE = "finance.db"

def get_db():
    # Reuse the same database connection during one request
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    # Run query with args, fetch results
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    # Return first result if one=True, else whole list
    return (rv[0] if rv else None) if one else rv

def init_db():
    # Open schema.sql and run all commands (create tables fresh)
    with sqlite3.connect(DATABASE) as db:
        with open("schema.sql", "r") as f:
            db.executescript(f.read())
