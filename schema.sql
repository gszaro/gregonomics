-- Reset everything by dropping old tables
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS debts;

-- User table holds login info
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Unique ID
    username TEXT NOT NULL UNIQUE,          -- Each username must be unique
    hash TEXT NOT NULL                      -- Hashed password
);

-- Track spending or income
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,               -- Link to user
    amount REAL NOT NULL,                   -- Could be positive (income) or negative (expense)
    category TEXT NOT NULL,                 -- e.g., food, rent, etc.
    note TEXT,                              -- Optional description
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, -- Auto-filled
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Debts table holds credit cards, loans, etc.
CREATE TABLE debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    balance REAL NOT NULL,                  -- Amount owed
    interest REAL NOT NULL,                 -- Interest rate %
    minimum REAL NOT NULL,                  -- Minimum monthly payment
    FOREIGN KEY(user_id) REFERENCES users(id)
);
