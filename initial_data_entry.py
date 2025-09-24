import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from dashboard.camera_data import (
    update_or_create_camera_data,
    get_custom_date_camera_data,
)
import subprocess
from django.utils import timezone
from django.db.models import Q
from dashboard.models import PeopleCounting, Cam

print("executed")
def ping_ip(ip, timeout=15):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 2,  # Overall timeout to avoid hanging
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timeout: Ping to {ip} took too long.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


ips = []
cams = Cam.objects.select_related("merchant", "branch").all()
for cam in cams:
    ips.append(
        {
            "ip": cam.ip,
            "cam_id": cam.pk,
            "merchant_id": cam.merchant.pk,
            "branch_id": cam.branch.pk,
        }
    )
for ip in ips:
    if ping_ip(ip["ip"]):
        try:
            data = get_custom_date_camera_data(ip["ip"], "2025-06-08", "2025-09-23") # change dates
            update_or_create_camera_data(
                data, ip["cam_id"], ip["merchant_id"], ip["branch_id"]
            )
            print("created")
        except Exception as e:
            print(e)
    else:
        print(f"This ip has a problem: {ip['ip']}")
