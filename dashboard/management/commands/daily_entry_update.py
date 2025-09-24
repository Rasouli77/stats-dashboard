from dashboard.models import PeopleCounting, Cam
from ...camera_data import update_or_create_camera_data, get_custom_date_camera_data
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
import logging
import subprocess
logger = logging.getLogger(__name__)

def ping_ip(ip, timeout=15):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 2  
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timeout: Ping to {ip} took too long.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

class Command(BaseCommand):
    help = "run daily update for entries"
    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        today_str = today.strftime("%Y-%m-%d")
        raw_yesterday = today - timedelta(days=1)
        yesterday = raw_yesterday.strftime("%Y-%m-%d")
        cams = Cam.objects.select_related("merchant", "branch").all()
        ips = []
        for cam in cams:
            ips.append({"ip": cam.ip, "cam_id": cam.pk, "merchant_id": cam.merchant.pk, "branch_id": cam.branch.pk})
        print(ips)
        for ip in ips:
            print(ip)
            if ping_ip(ip['ip']):
                print(ip['ip'])
                try:
                    data = get_custom_date_camera_data(ip["ip"], today_str, today_str)
                    update_or_create_camera_data(data, ip["cam_id"], ip["merchant_id"], ip["branch_id"])
                except Exception as e:
                    print(e)
            else:
                print(f"This ip has a problem: {ip['ip']}")
