from .dahua_rpc import DahuaRpc
from datetime import datetime, timedelta

def get_camera_data(ip:str):
    """
    It requires an IP as an arguemnet to return a dictionary if username and password are correct
    """
    dahua = DahuaRpc(host=ip, username="pc", password="@123456789")
    dahua.login()
    dahua.current_time()
    dahua.request(method="magicBox.getSerialNo")
    object_id = dahua.get_people_counting_info()
    start_date = datetime(2025, 1, 20)
    end_date = datetime(2025, 5, 13)

    date_ranges = []

    current = start_date
    while current <= end_date:
        day_str = current.strftime("%Y-%m-%d")
        date_ranges.append((f"{day_str}T00:00:00Z", f"{day_str}T23:59:59Z"))
        current += timedelta(days=1)

    sum_of_entries = {}
    for date in date_ranges:
        totalCount = dahua.start_find_statistics_data(object_id, date[0], date[1], 1)
        items = dahua.do_find_statistics_data(object_id)
        sum = 0
        for item in items:
            sum += item['EnteredSubtotal']
            key_date = datetime.strptime(date[0], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
            sum_of_entries[key_date] = sum
    return sum_of_entries
