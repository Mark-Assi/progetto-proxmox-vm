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
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'admin'))
);
""")

print("Creo tabella 'requests'...")

c.execute("""
CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    criterio TEXT NOT NULL,
    tipo_vm TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',

    vm_id TEXT,
    hostname TEXT,
    ip_address TEXT,
    vm_username TEXT,
    vm_password TEXT,
    ssh_key TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

# Aggiunta utenti di test
print("Inserisco utenti di test...")

c.execute("""
INSERT INTO users (username, email, password, role)
VALUES (?, ?, ?, ?)
""", ("user", "user@example.com", "user123", "user"))

c.execute("""
INSERT INTO users (username, email, password, role)
VALUES (?, ?, ?, ?)
""", ("admin", "admin@example.com", "admin123", "admin"))

conn.commit()
conn.close()

print("Database creato con successo!")
