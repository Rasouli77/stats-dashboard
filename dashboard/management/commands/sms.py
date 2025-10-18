from kavenegar import *
import os
from dotenv import load_dotenv
from dashboard.models import Cam
import subprocess
from django.core.management.base import BaseCommand
import logging

# Load Environment Variables
load_dotenv()

# Kavenegar API key
KAVENEGAR_API = os.environ.get("KAVENEGAR_API")


def ping_ip(ip, timeout=15):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 2,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timeout: Ping to {ip} took too long.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def find_broken_ips(merchant_hash):
    broken_ips = []
    cameras = Cam.objects.filter(
        merchant__url_hash=merchant_hash
    )  # change this later according to the merchant's hash
    for camera in cameras:
        camera.status = ping_ip(camera.ip)
        if camera.status == True:
            broken_ips.append(camera.ip)
        camera.save()
    return broken_ips


def send_camera_malfunction_alert(mobile: str, broken_cam_ips: list):
    broken_cam_ips = [item for item in broken_cam_ips if item is not None]
    mobile = [
        mobile,
    ]
    token = ",".join(broken_cam_ips)
    try:
        api = KavenegarAPI(KAVENEGAR_API)
        params = {
            'sender': '', 
            'receptor': '09126997470', # change this to mobile with the existing format
            'template': 'alert', 
            'token': token
        }
        response = api.verify_lookup(params)
        print(response)
    except Exception as e:
        print(e)
        pass
    except APIException as e:
        print(f"APIException: {e}")
        return {"error": str(e)}
    except HTTPException as e:
        print(f"HTTPException: {e}")
        return {"error": str(e)}



class Command(BaseCommand):
    help = "send sms of broken ips"

    def handle(self, *args, **kwargs):
        broken_camera_ips = find_broken_ips("4CbCwLRPAJ5B") # change this hash later accordingly
        print(broken_camera_ips)
        send_camera_malfunction_alert("9361413096", broken_camera_ips)
