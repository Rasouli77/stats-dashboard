from dashboard.models import Stats
from ...camera_data import get_camera_data, merge_camera_data, create_camera_data_record
from datetime import datetime
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "run daily update for entries"
    def handle(self, *args, **kwargs):
        print(f"running daily update at {datetime.now()}")
        # Branches with one camera installed
        aghdasieh_entry = get_camera_data("172.16.20.103")
        mehrad_entry = get_camera_data("172.16.90.241")
        # Branches with two cameras
        iran_mall_one = get_camera_data("172.16.70.75")
        iran_mall_two = get_camera_data("172.16.70.128")
        hadish_mall_one = get_camera_data("172.16.40.174")
        hadish_mall_two = get_camera_data("172.16.40.175")
        # They need to be merged
        iran_mall_entry = merge_camera_data(iran_mall_one, iran_mall_two)
        hadish_mall_entry = merge_camera_data(hadish_mall_one, hadish_mall_two)
        print(aghdasieh_entry, mehrad_entry, iran_mall_entry, hadish_mall_entry)
        create_camera_data_record(aghdasieh_entry, "وب پوش", "اقدسیه")
        create_camera_data_record(mehrad_entry, "وب پوش", "مهراد مال")
        create_camera_data_record(iran_mall_entry, "وب پوش", "ایران مال")
        create_camera_data_record(hadish_mall_entry, "وب پوش", "هدیش مال")
        print("sucessfully created")


