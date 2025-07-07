from dashboard.models import PeopleCounting, Cam
from ...camera_data import update_or_create_camera_data, get_custom_date_camera_data
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = "run daily update for entries"
    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        raw_yesterday = today - timedelta(days=1)
        yesterday = raw_yesterday.strftime("%Y-%m-%d")
        cams = Cam.objects.select_related("merchant", "branch").all()
        ips = []
        for cam in cams:
            ips.append({"ip": cam.ip, "cam_id": cam.pk, "merchant_id": cam.merchant.pk, "branch_id": cam.branch.pk})

        for ip in ips:
            data = get_custom_date_camera_data(ip["ip"], yesterday, yesterday)
            update_or_create_camera_data(data, ip["cam_id"], ip["merchant_id"], ip["branch_id"])
        


        


