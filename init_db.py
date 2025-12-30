import sqlite3
import os

DB_NAME = "proxmox-progetto.db"

if os.path.exists(DB_NAME):
    import sqlite3
    import os

    DB_NAME = "proxmox-progetto.db"

    if os.path.exists(DB_NAME):
        print("Elimino il database esistente...")
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

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

    print("Creo tabella 'vm_templates'...")

    c.execute("""
    CREATE TABLE vm_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        cpu INTEGER NOT NULL,
        memory_mb INTEGER NOT NULL,
        disk_gb INTEGER NOT NULL,
        description TEXT
    );
    """)

    print("Creo tabella 'requests'...")

    c.execute("""
    CREATE TABLE requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        template_type TEXT NOT NULL,
        hostname TEXT,
        status TEXT NOT NULL DEFAULT 'pending',
        proxmox_vmid INTEGER,
        ip_address TEXT,
        vm_username TEXT,
        vm_password TEXT,
        ssh_key TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (template_type) REFERENCES vm_templates(name)
    );
    """)

    print("Inserisco template VM di esempio...")

    c.execute("""
    INSERT INTO vm_templates (name, cpu, memory_mb, disk_gb, description)
    VALUES (?, ?, ?, ?, ?)
    """, ("Bronze", 1, 1024, 8, "Base - 1 vCPU, 1GB RAM, 8GB disk"))

    c.execute("""
    INSERT INTO vm_templates (name, cpu, memory_mb, disk_gb, description)
    VALUES (?, ?, ?, ?, ?)
    """, ("Silver", 2, 4096, 20, "Intermedio - 2 vCPU, 4GB RAM, 20GB disk"))

    c.execute("""
    INSERT INTO vm_templates (name, cpu, memory_mb, disk_gb, description)
    VALUES (?, ?, ?, ?, ?)
    """, ("Gold", 4, 8192, 40, "Prestazioni - 4 vCPU, 8GB RAM, 40GB disk"))

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