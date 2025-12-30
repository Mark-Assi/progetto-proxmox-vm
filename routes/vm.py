from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from utils.database import create_request

vm = Blueprint("vm", __name__)

@vm.route("/request-vm", methods=["GET", "POST"])
@login_required
def request_vm():
    if request.method == "POST":
        template_type = request.form.get("template_type")

        create_request(current_user.id, template_type)

        return render_template("confirm_vm.html", template_type=template_type)

    return render_template("request_vm.html")