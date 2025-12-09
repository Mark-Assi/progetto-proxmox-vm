from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from utils.database import create_request

vm = Blueprint("vm", __name__)

@vm.route("/request-vm", methods=["GET", "POST"])
@login_required
def request_vm():
    if request.method == "POST":
        criterio = request.form.get("criterio")
        tipo_vm = request.form.get("tipo_vm")

        # salvarla nel DB
        create_request(current_user.id, criterio, tipo_vm)

        return render_template("confirm_vm.html", criterio=criterio, tipo_vm=tipo_vm)

    return render_template("request_vm.html")
