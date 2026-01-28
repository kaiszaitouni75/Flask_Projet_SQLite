import sqlite3

conn = sqlite3.connect("bibliotheque.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT,
    auteur TEXT,
    stock INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_id INTEGER
)
""")

# Comptes de test
cursor.execute("INSERT INTO users VALUES (NULL,'admin','admin','admin')")
cursor.execute("INSERT INTO users VALUES (NULL,'user','12345','user')")

conn.commit()
conn.close()

print("Base bibliothèque créée")
