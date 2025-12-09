import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = "supersegreto"

DB_NAME = "proxmox-progetto.db"

# --- LOGIN SETUP ---
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Classe utente Flask
class User(UserMixin):
    def __init__(self, user_id, username, email, role):
        self.id = user_id
        self.username = username
        self.email = email
        self.role = role

def get_user_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, username, email, password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row  # (id, username, email, password)

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()

    if row:
        return User(row[0], row[1], row[2])
    return None

# --- ROUTES ---

# ROOT = LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_row = get_user_by_username(username)

        if user_row and user_row[3] == password:
            user = User(user_row[0], user_row[1], user_row[2])
            login_user(user)
            return redirect(url_for("dashboard"))

        return "Credenziali errate"

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/request-vm", methods=["GET", "POST"])
@login_required
def request_vm():
    if request.method == "POST":
        criterio = request.form.get("criterio")
        tipo_vm = request.form.get("tipo_vm")

        return render_template("confirm_vm.html", criterio=criterio, tipo_vm=tipo_vm)

    return render_template("request_vm.html")

if __name__ == "__main__":
    app.run(debug=True)


