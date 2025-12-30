import os
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv

load_dotenv()

PROXMOX_HOST = os.getenv('PROXMOX_HOST')
PX_USERNAME = os.getenv('PX_USERNAME')
TOKEN_NAME = os.getenv('TOKEN_NAME')
PROXMOX_TOKEN_SECRET = os.getenv('PROXMOX_TOKEN_SECRET')
CT_TEMPLATE_ID = os.getenv('CT_TEMPLATE_ID')
CT_STORAGE = os.getenv('CT_STORAGE', 'local')
VERIFY_SSL = os.getenv('PROXMOX_VERIFY_SSL', 'false').lower() == 'true'

if not PROXMOX_HOST or not PX_USERNAME or not TOKEN_NAME or not PROXMOX_TOKEN_SECRET:
    print("Warning: alcune variabili Proxmox non sono settate. Verifica il file .env")

def _get_proxmox():
    return ProxmoxAPI(PROXMOX_HOST, user=PX_USERNAME, token_name=TOKEN_NAME, token_value=PROXMOX_TOKEN_SECRET, verify_ssl=VERIFY_SSL)

def create_lxc_from_template(template_id, name, cpu=None, memory_mb=None, disk_gb=None):
    """Clona il template LXC e applica risorse. Ritorna il nuovo VMID (int).

    Nota: questa funzione assume che il template sia un container LXC e che
    esista almeno un nodo nel cluster. Usa il primo nodo trovato.
    """
    proxmox = _get_proxmox()

    nodes = proxmox.nodes.get()
    if not nodes:
        raise RuntimeError("Nessun nodo Proxmox disponibile")
    node = nodes[0]['node']

    nextid = proxmox.cluster.nextid.get()

    clone_params = {
        'newid': nextid,
        'name': name,
        'full': 1,
        'storage': CT_STORAGE,
    }

    upid = proxmox.nodes(node).lxc(template_id).clone.post(**clone_params)

    try:
        task_upid = upid.get('upid') if isinstance(upid, dict) else upid
    except Exception:
        task_upid = upid

    if cpu is not None or memory_mb is not None or disk_gb is not None:
        cfg = {}
        if cpu is not None:
            cfg['cores'] = int(cpu)
        if memory_mb is not None:
            cfg['memory'] = int(memory_mb)
        if disk_gb is not None:
            cfg['rootfs'] = f"{CT_STORAGE}:{int(disk_gb)}G"

        try:
            proxmox.nodes(node).lxc(nextid).config.post(**cfg)
        except Exception:
            pass

    return int(nextid)