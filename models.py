import sqlite3
from flask import g

DATABASE = "finance.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with sqlite3.connect(DATABASE) as db:
        with open("schema.sql", "r") as f:
            db.executescript(f.read())
