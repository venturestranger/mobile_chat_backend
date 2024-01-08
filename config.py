class Config:
	PORT = 7890
	ASSETS = "./storage/assets/"
	DB = "./storage/data.db"
	DB_INIT = True
	DB_TEMPLATE ="""
DROP TABLE IF EXISTS users
---
DROP TABLE IF EXISTS messages
---
DROP TABLE IF EXISTS followers
---
CREATE TABLE users (
id INTEGER PRIMARY KEY,
login TEXT NOT NULL,
password TEXT NOT NULL,
about TEXT NOT NULL
)
---
CREATE TABLE followers (
id INTEGER PRIMARY KEY,
user_from INTEGER NOT NULL,
user_to INTEGER NOT NULL,
FOREIGN KEY(user_from) REFERENCES users(id),
FOREIGN KEY(user_to) REFERENCES users(id)
)
---
CREATE TABLE messages (
id INTEGER PRIMARY KEY,
user_from INTEGER NOT NULL,
user_to INTEGER NOT NULL,
type INTEGER NOT NULL,
content text,
FOREIGN KEY(user_from) REFERENCES users(id),
FOREIGN KEY(user_to) REFERENCES users(id)
)
"""
