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

def create_request(user_id, template_type):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO requests (user_id, template_type)
        VALUES (?, ?)
    """, (user_id, template_type))

    conn.commit()
    conn.close()

def get_request_by_id(request_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT id, user_id, template_type, hostname, status, proxmox_vmid, ip_address, created_at
        FROM requests
        WHERE id = ?
    """, (request_id,))
    row = c.fetchone()
    conn.close()
    return row

def delete_request(request_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM requests WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()

def update_request_after_create(request_id, proxmox_vmid, ip_address=None, status='active'):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE requests
        SET proxmox_vmid = ?, ip_address = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (proxmox_vmid, ip_address, status, request_id))
    conn.commit()
    conn.close()

def get_vm_template_by_name(name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, cpu, memory_mb, disk_gb, description FROM vm_templates WHERE name = ?", (name,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_requests():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT r.id, u.username, r.template_type, r.status, r.created_at
        FROM requests r
        JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
    """)

    rows = c.fetchall()
    conn.close()
    return rows