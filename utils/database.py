import sqlite3

DB_NAME = "proxmox-progetto.db"

def get_connection():
    """Restituisce una connessione al database."""
    return sqlite3.connect(DB_NAME)


def get_user_by_username(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, password, role FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row


def get_user_by_id(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def create_request(user_id, criterio, tipo_vm):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO requests (user_id, criterio, tipo_vm)
        VALUES (?, ?, ?)
    """, (user_id, criterio, tipo_vm))

    conn.commit()
    conn.close()

def get_all_requests():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT r.id, u.username, r.criterio, r.tipo_vm, r.status, r.created_at
        FROM requests r
        JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
    """)

    rows = c.fetchall()
    conn.close()
    return rows
