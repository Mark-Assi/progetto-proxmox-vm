from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from utils.database import get_all_requests, get_request_by_id, delete_request, get_vm_template_by_name, update_request_after_create
from utils.proxmox import create_lxc_from_template

admin = Blueprint("admin", __name__)

@admin.route("/admin/requests")
@login_required
def admin_requests():
    if current_user.role != "admin":
        return "Non autorizzato", 403

    richieste = get_all_requests()

    return render_template("admin_requests.html", richieste=richieste)

@admin.route('/admin/requests/<int:request_id>/reject', methods=['POST'])
@login_required
def reject_request(request_id):
    if current_user.role != 'admin':
        return "Non autorizzato", 403

    delete_request(request_id)
    return redirect(url_for('admin.admin_requests'))

@admin.route('/admin/requests/<int:request_id>/approve', methods=['POST'])
@login_required
def approve_request(request_id):
    if current_user.role != 'admin':
        return "Non autorizzato", 403

    req = get_request_by_id(request_id)
    if not req:
        return "Richiesta non trovata", 404

    _, user_id, template_type, hostname, status, _, _, _ = req

    tpl = get_vm_template_by_name(template_type)
    if not tpl:
        return "Template non trovato", 500

    _, name, cpu, memory_mb, disk_gb, _desc = tpl

    if not hostname:
        hostname = f"{name.lower()}-{request_id}"

    try:
        vmid = create_lxc_from_template(int(__import__('os').getenv('CT_TEMPLATE_ID')), hostname, cpu=cpu, memory_mb=memory_mb, disk_gb=disk_gb)
    except Exception as e:
        return f"Errore creazione VM: {e}", 500

    update_request_after_create(request_id, vmid, ip_address=None, status='active')

    return redirect(url_for('admin.admin_requests'))
