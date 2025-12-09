from flask import Blueprint, render_template
from flask_login import login_required, current_user
from utils.database import get_all_requests

admin = Blueprint("admin", __name__)

@admin.route("/admin/requests")
@login_required
def admin_requests():
    if current_user.role != "admin":
        return "Non autorizzato", 403

    richieste = get_all_requests()

    return render_template("admin_requests.html", richieste=richieste)

