from .dahua_rpc import DahuaRpc
from datetime import datetime, timedelta
from .models import PeopleCounting, Cam, Merchant, Branch

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

def create_camera_data_record(data:dict):
    """
    This function takes a dictionary, vendor and branch, then it turns into a PeopleCounting Object.
    """
    for date in data.items():
        print(date[1]["date"], date[1]["entry"], date[1]["exit"])
        
        
        
        
def get_custom_date_camera_data(ip:str, start_date_str: str, end_date_str:str):
    """
    This function takes an IP, a start date and an end date. It returns a dictionary of dates and total entries for a date
    """
    dahua = DahuaRpc(host=ip, username="pc", password="@123456789")
    dahua.login()
    dahua.current_time()
    dahua.request(method="magicBox.getSerialNo")
    object_id = dahua.get_people_counting_info()
    dicts = {}
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end_date - start_date).days + 1)]
    for date in dates:
        totalCount = dahua.start_find_statistics_data(object_id, f"{date}T00:00:00Z", f"{date}T23:59:59Z", 1)
        items = dahua.do_find_statistics_data(object_id)
        sum_entry = 0
        sum_exit = 0
        for item in items:
            sum_entry += item['EnteredSubtotal']
            sum_exit += item['ExitedSubtotal']
            each_date = datetime.strptime(f"{date}", "%Y-%m-%d").strftime("%Y-%m-%d")
            dicts[each_date] = {
                "date": each_date,
                "entry": sum_entry,
                "exit": sum_exit
            }
    return dicts

def update_or_create_camera_data(data: dict, cam_id, merchant_id, branch_id):
    cam = Cam.objects.select_related().get(pk=cam_id)
    merchant = Merchant.objects.select_related().get(pk=merchant_id)
    branch = Branch.objects.select_related().get(pk=branch_id)
    for date in data.items():
        PeopleCounting.objects.update_or_create(
            date=date[1]["date"],
            entry=date[1]["entry"],
            exit=date[1]["exit"],
            cam=cam,
            merchant=merchant,
            branch=branch
            )
        