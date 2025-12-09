import sqlite3
import os

DB_NAME = "proxmox-progetto.db"

# Se esiste già, lo elimina
if os.path.exists(DB_NAME):
    print("Elimino il database esistente...")
    os.remove(DB_NAME)

# Crea nuovo DB
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

print("Creo tabella 'users'...")

c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);
""")

# Aggiungiamo 2 utenti di test
c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
          ("user", "user@example.com", "user123"))
c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
          ("admin", "admin@example.com", "admin123"))

conn.commit()
conn.close()

print("Database creato con successo!")