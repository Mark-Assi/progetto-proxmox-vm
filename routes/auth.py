from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from utils.database import get_user_by_username, get_user_by_id

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_row = get_user_by_username(username)

        if user_row and user_row[3] == password:
            user = User(user_row[0], user_row[1], user_row[2], user_row[4])
            login_user(user)
            return redirect(url_for("auth.dashboard"))

        return "Credenziali errate"

    return render_template("login.html")


@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
