import os
import django
from dashboard.models import HolidayDate, HolidayDescription
import requests
import jdatetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def get_jalali_dates(start_date: str, end_date: str):
    start_date = jdatetime.datetime.strptime(start_date, "%Y/%m/%d")
    end_date = jdatetime.datetime.strptime(end_date, "%Y/%m/%d")
    dates = []
    current = start_date
    while current <= end_date:
        dates.append(current.strftime("%Y/%m/%d"))
        current += jdatetime.timedelta(days=1)
    return dates

all_dates = get_jalali_dates("1405/01/01", "1405/12/29")

def holidays_spotter(dates):
    for date in dates:
        print(date)
        year = date[0:4]
        month = date[5:7]
        day = date[8:]
        try:
            response = requests.get(f"http://127.0.0.1:8000/api/holiday-spotter/{year}/{month}/{day}", timeout=10)
            print(f"http://127.0.0.1:8000/api/holiday-spotter/{year}/{month}/{day}")
            if response.status_code == 200:
                data = response.json()
                if data["is_holiday"] == True:
                    jalali_date = jdatetime.datetime.strptime(date, "%Y/%m/%d").date()
                    gregorian_date = jalali_date.togregorian()
                    this_date = HolidayDate.objects.update_or_create(date=date, defaults={"gregorian_date": gregorian_date})
                    print(f"{date} was successfuly created.")
                    events = data["events"] if data["events"] else []
                    if events:
                        for event in events:
                            HolidayDescription.objects.create(date=this_date, description=event["description"])
                            print(f"{event} was successfully created for {date}.")
        except Exception as e:
            print(e)

holidays_spotter(all_dates)
