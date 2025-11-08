from .dahua_rpc import DahuaRpc
from datetime import datetime, timedelta
from .models import PeopleCounting, Cam, Merchant, Branch


def get_camera_data(ip: str):
    """
    It requires an IP as an arguemnet to return a dictionary if username and password are correct. It returns yesterday's numbers.
    """
    dahua = DahuaRpc(host=ip, username="pc", password="@123456789")
    dahua.login()
    dahua.current_time()
    dahua.request(method="magicBox.getSerialNo")
    object_id = dahua.get_people_counting_info()
    today = datetime.now().date()
    totalCount = dahua.start_find_statistics_data(
        object_id, f"{today}T00:00:00Z", f"{today}T23:59:59Z", 1
    )
    items = dahua.do_find_statistics_data(object_id)
    print(items)
    result = []
    for item in items:
        dictionary = {}
        dt = datetime.strptime(item['EndTime'], "%Y-%m-%d %H:%M:%S")
        y, m, d = dt.year, dt.month, dt.day
        date = f"{y}/{m}/{d}"
        dt = dt + timedelta(seconds=1)
        dt = dt.strftime("%H:%M:%S")
        dictionary["date"] = date
        dictionary[dt] = item['EnteredSubtotal']
        result.append(dictionary)
    print(result)
    return result


def merge_camera_data(entries_one: dict, entries_two: dict):
    """
    This function merges the data gathered from two cameras.
    """
    return {key: entries_one[key] + entries_two[key] for key in entries_one}


def create_camera_data_record(data: dict):
    """
    This function takes a dictionary, vendor and branch, then it turns into a PeopleCounting Object.
    """
    for date in data.items():
        print(date[1]["date"], date[1]["entry"], date[1]["exit"])


def get_custom_date_camera_data(ip: str, start_date_str: str, end_date_str: str):
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
    dates = [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((end_date - start_date).days + 1)
    ]
    for date in dates:
        totalCount = dahua.start_find_statistics_data(
            object_id, f"{date}T00:00:00Z", f"{date}T23:59:59Z", 1
        )
        items = dahua.do_find_statistics_data(object_id)
        sum_entry = 0
        sum_exit = 0
        for item in items:
            sum_entry += item["EnteredSubtotal"]
            sum_exit += item["ExitedSubtotal"]
            each_date = datetime.strptime(f"{date}", "%Y-%m-%d").strftime("%Y-%m-%d")
            dicts[each_date] = {"date": each_date, "entry": sum_entry, "exit": sum_exit}
    return dicts


def update_or_create_camera_data(data: dict, cam_id, merchant_id, branch_id):
    cam = Cam.objects.select_related().get(pk=cam_id)
    merchant = Merchant.objects.select_related().get(pk=merchant_id)
    branch = Branch.objects.select_related().get(pk=branch_id)
    for date in data.items():
        PeopleCounting.objects.update_or_create(
            date=date[1]["date"],
            cam=cam,
            defaults={
                "entry": date[1]["entry"],
                "exit": date[1]["exit"],
                "merchant": merchant,
                "branch": branch,
            },
        )


def get_custom_date_camera_data_hour(ip: str, start_date_str: str, end_date_str: str):
    """
    This function takes an IP, a start date and an end date. It returns a dictionary of dates and total entries for a date
    """
    dahua = DahuaRpc(host=ip, username="pc", password="@123456789")
    dahua.login()
    dahua.current_time()
    dahua.request(method="magicBox.getSerialNo")
    object_id = dahua.get_people_counting_info()
    dicts = []
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    dates = [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((end_date - start_date).days + 1)
    ]
    hour_entry_avg = {
        "01:00:00": 0,
        "02:00:00": 0,
        "03:00:00": 0,
        "04:00:00": 0,
        "05:00:00": 0,
        "06:00:00": 0,
        "07:00:00": 0,
        "08:00:00": 0,
        "09:00:00": 0,
        "10:00:00": 0,
        "11:00:00": 0,
        "12:00:00": 0,
        "13:00:00": 0,
        "14:00:00": 0,
        "15:00:00": 0,
        "16:00:00": 0,
        "17:00:00": 0,
        "18:00:00": 0,
        "19:00:00": 0,
        "20:00:00": 0,
        "21:00:00": 0,
        "22:00:00": 0,
        "23:00:00": 0
    }
    for date in dates:
        totalCount = dahua.start_find_statistics_data(
            object_id, f"{date}T00:00:00Z", f"{date}T23:59:59Z", 1
        )
        items = dahua.do_find_statistics_data(object_id)
        sum_entry = 0
        sum_exit = 0
        for item in items:
            # hey
            print(item)
            dictionary = {}
            dt = datetime.strptime(item['EndTime'], "%Y-%m-%d %H:%M:%S")
            dt = dt + timedelta(seconds=1)
            d = dt.strftime("%Y-%m-%d")
            dt = dt.strftime("%H:%M:%S")
            dictionary["date"] = d
            dictionary['hour'] = dt
            dictionary['entry'] = item['EnteredSubtotal']
            dicts.append(dictionary)

    if start_date_str == end_date_str:
        return dicts

    date_list = []
    for item in dicts:
        if item['date'] not in date_list:
            date_list.append(item['date'])

    for item in dicts:
        hour_entry_avg[item['hour']] += item['entry'] / len(date_list)
    print(hour_entry_avg)
    print(dicts)
    return dicts


# [{'date': '2025-11-01', 'hour': '01:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '02:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '03:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '04:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '05:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '06:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '07:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '08:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '09:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '10:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '11:00:00', 'entry': 5}, {'date': '2025-11-01', 'hour': '12:00:00', 'entry': 8}, {'date': '2025-11-01', 'hour': '13:00:00', 'entry': 5}, {'date': '2025-11-01', 'hour': '14:00:00', 'entry': 4}, {'date': '2025-11-01', 'hour': '15:00:00', 'entry': 5}, {'date': '2025-11-01', 'hour': '16:00:00', 'entry': 3}, {'date': '2025-11-01', 'hour': '17:00:00', 'entry': 10}, {'date': '2025-11-01', 'hour': '18:00:00', 'entry': 7}, {'date': '2025-11-01', 'hour': '19:00:00', 'entry': 6}, {'date': '2025-11-01', 'hour': '20:00:00', 'entry': 2}, {'date': '2025-11-01', 'hour': '21:00:00', 'entry': 0}, {'date': '2025-11-01', 'hour': '22:00:00', 'entry': 1}, {'date': '2025-11-01', 'hour': '23:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '01:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '02:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '03:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '04:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '05:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '06:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '07:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '08:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '09:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '10:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '11:00:00', 'entry': 7}, {'date': '2025-11-02', 'hour': '12:00:00', 'entry': 6}, {'date': '2025-11-02', 'hour': '13:00:00', 'entry': 3}, {'date': '2025-11-02', 'hour': '14:00:00', 'entry': 7}, {'date': '2025-11-02', 'hour': '15:00:00', 'entry': 6}, {'date': '2025-11-02', 'hour': '16:00:00', 'entry': 5}, {'date': '2025-11-02', 'hour': '17:00:00', 'entry': 7}, {'date': '2025-11-02', 'hour': '18:00:00', 'entry': 1}, {'date': '2025-11-02', 'hour': '19:00:00', 'entry': 8}, {'date': '2025-11-02', 'hour': '20:00:00', 'entry': 7}, {'date': '2025-11-02', 'hour': '21:00:00', 'entry': 0}, {'date': '2025-11-02', 'hour': '22:00:00', 'entry': 5}, {'date': '2025-11-02', 'hour': '23:00:00', 'entry': 1}, {'date': '2025-11-03', 'hour': '01:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '02:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '03:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '04:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '05:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '06:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '07:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '08:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '09:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '10:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '11:00:00', 'entry': 4}, {'date': '2025-11-03', 'hour': '12:00:00', 'entry': 3}, {'date': '2025-11-03', 'hour': '13:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '14:00:00', 'entry': 1}, {'date': '2025-11-03', 'hour': '15:00:00', 'entry': 1}, {'date': '2025-11-03', 'hour': '16:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '17:00:00', 'entry': 2}, {'date': '2025-11-03', 'hour': '18:00:00', 'entry': 5}, {'date': '2025-11-03', 'hour': '19:00:00', 'entry': 0}, {'date': '2025-11-03', 'hour': '20:00:00', 'entry': 4}, {'date': '2025-11-03', 'hour': '21:00:00', 'entry': 9}, {'date': '2025-11-03', 'hour': '22:00:00', 'entry': 7}, {'date': '2025-11-03', 'hour': '23:00:00', 'entry': 3}, {'date': '2025-11-04', 'hour': '01:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '02:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '03:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '04:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '05:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '06:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '07:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '08:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '09:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '10:00:00', 'entry': 0}, {'date': '2025-11-04', 'hour': '11:00:00', 'entry': 5}, {'date': '2025-11-04', 'hour': '12:00:00', 'entry': 8}, {'date': '2025-11-04', 'hour': '13:00:00', 'entry': 4}, {'date': '2025-11-04', 'hour': '14:00:00', 'entry': 6}, {'date': '2025-11-04', 'hour': '15:00:00', 'entry': 11}, {'date': '2025-11-04', 'hour': '16:00:00', 'entry': 6}, {'date': '2025-11-04', 'hour': '17:00:00', 'entry': 3}, {'date': '2025-11-04', 'hour': '18:00:00', 'entry': 8}, {'date': '2025-11-04', 'hour': '19:00:00', 'entry': 5}, {'date': '2025-11-04', 'hour': '20:00:00', 'entry': 2}, {'date': '2025-11-04', 'hour': '21:00:00', 'entry': 15}, {'date': '2025-11-04', 'hour': '22:00:00', 'entry': 2}, {'date': '2025-11-04', 'hour': '23:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '01:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '02:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '03:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '04:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '05:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '06:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '07:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '08:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '09:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '10:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '11:00:00', 'entry': 2}, {'date': '2025-11-05', 'hour': '12:00:00', 'entry': 3}, {'date': '2025-11-05', 'hour': '13:00:00', 'entry': 2}, {'date': '2025-11-05', 'hour': '14:00:00', 'entry': 0}, {'date': '2025-11-05', 'hour': '15:00:00', 'entry': 3}, {'date': '2025-11-05', 'hour': '16:00:00', 'entry': 3}, {'date': '2025-11-05', 'hour': '17:00:00', 'entry': 1}, {'date': '2025-11-05', 'hour': '18:00:00', 'entry': 3}, {'date': '2025-11-05', 'hour': '19:00:00', 'entry': 9}, {'date': '2025-11-05', 'hour': '20:00:00', 'entry': 10}, {'date': '2025-11-05', 'hour': '21:00:00', 'entry': 8}, {'date': '2025-11-05', 'hour': '22:00:00', 'entry': 6}, {'date': '2025-11-05', 'hour': '23:00:00', 'entry': 0}]