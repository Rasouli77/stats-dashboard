from .dahua_rpc import DahuaRpc
from datetime import datetime, timedelta
from .models import Stats

def get_camera_data(ip:str):
    """
    It requires an IP as an arguemnet to return a dictionary if username and password are correct. It returns yesterday's numbers.
    """
    dahua = DahuaRpc(host=ip, username="pc", password="@123456789")
    dahua.login()
    dahua.current_time()
    dahua.request(method="magicBox.getSerialNo")
    object_id = dahua.get_people_counting_info()
    sum_of_entries = {}
    yesterday = datetime.now().date() - timedelta(1)
    totalCount = dahua.start_find_statistics_data(object_id, f"{yesterday}T00:00:00Z", f"{yesterday}T23:59:59Z", 1)
    items = dahua.do_find_statistics_data(object_id)
    sum = 0
    for item in items:
        sum += item['EnteredSubtotal']
        key_date = datetime.strptime(f"{yesterday}", "%Y-%m-%d").strftime("%Y-%m-%d")
        sum_of_entries[key_date] = sum
    return sum_of_entries

def merge_camera_data(entries_one:dict, entries_two:dict):
    """
    This function merges the data gathered from two cameras.
    """
    return {key: entries_one[key] + entries_two[key] for key in entries_one}

def create_camera_data_record(data:dict, vendor: str, branch:str):
    """
    This function takes a dictionary, vendor and branch, then it turns into a Stats Object.
    """
    for date, entry in data.items():
        Stats.objects.update_or_create(
            date=date,
            entry=entry,
            vendor=vendor,
            branch=branch
        )