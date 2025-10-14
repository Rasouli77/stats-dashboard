import jdatetime
import re
from collections import defaultdict

y = [684, 769, 755, 792, 1257, 1853, 2792, 797, 740, 798, 742, 801, 1873, 3014, 646, 681, 768, 737, 1049, 1563, 2395, 660, 618, 533, 810, 752, 1695, 2481, 547, 593, 742, 697, 759, 1351, 2113]
x = ['۱۴۰۴/۰۴/۲۸', '۱۴۰۴/۰۴/۲۹', '۱۴۰۴/۰۴/۳۰', '۱۴۰۴/۰۴/۳۱', '۱۴۰۴/۰۵/۰۱', '۱۴۰۴/۰۵/۰۲', '۱۴۰۴/۰۵/۰۳', '۱۴۰۴/۰۵/۰۴', '۱۴۰۴/۰۵/۰۵', '۱۴۰۴/۰۵/۰۶', '۱۴۰۴/۰۵/۰۷', '۱۴۰۴/۰۵/۰۸', '۱۴۰۴/۰۵/۰۹', '۱۴۰۴/۰۵/۱۰', '۱۴۰۴/۰۵/۱۱', '۱۴۰۴/۰۵/۱۲', '۱۴۰۴/۰۵/۱۳', '۱۴۰۴/۰۵/۱۴', '۱۴۰۴/۰۵/۱۵', '۱۴۰۴/۰۵/۱۶', '۱۴۰۴/۰۵/۱۷', '۱۴۰۴/۰۵/۱۸', '۱۴۰۴/۰۵/۱۹', '۱۴۰۴/۰۵/۲۰', '۱۴۰۴/۰۵/۲۱', '۱۴۰۴/۰۵/۲۲', '۱۴۰۴/۰۵/۲۳', '۱۴۰۴/۰۵/۲۴', '۱۴۰۴/۰۵/۲۵', '۱۴۰۴/۰۵/۲۶', '۱۴۰۴/۰۵/۲۷', '۱۴۰۴/۰۵/۲۸', '۱۴۰۴/۰۵/۲۹', '۱۴۰۴/۰۵/۳۰', '۱۴۰۴/۰۵/۳۱']
PERSIAN_TO_ENGLISH_MAPPING = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹",
    "0123456789"
)
ENGLISH_TO_PERSIAN_MAPPING = str.maketrans(
    "0123456789",
    "۰۱۲۳۴۵۶۷۸۹"
)

def ascii_to_persian(s: str) -> str:
    s = s.strip()
    return s.translate(ENGLISH_TO_PERSIAN_MAPPING)


def persian_to_ascii(s: str) -> str:
    s = s.strip()
    return s.translate(PERSIAN_TO_ENGLISH_MAPPING)


def persian_date_to_jdate(s: str):
    s = persian_to_ascii(s)
    parts = re.split(r'[\/\-\.]', s)
    y, m, d = map(int, parts)
    return jdatetime.date(y, m, d)


def divide_monthly(dates, values):
    monthly_data = defaultdict(int)
    for d, v in zip(dates, values):
        date = persian_date_to_jdate(d)
        year = date.year
        month = date.month
        if len(str(month)) == 1:
            key = f'{year}/0{month}'
        else:
            key = f'{year}/{month}'
        monthly_data[key] += v
    sorted_monthly_data = sorted(monthly_data.items(), key=lambda item: int(re.sub("/", "", item[0])))
    monthly_data = dict(sorted_monthly_data)
    monthly_data_output = {}
    for k, v in monthly_data.items():
        monthly_data_output[ascii_to_persian(k)] = v 
    months = list(monthly_data_output.keys())
    values = list(monthly_data_output.values())
    return months, values


def divide_weekly(dates, values):
    weekly_data = defaultdict(int)
    for d, v in zip(dates, values):
        date = persian_date_to_jdate(d)
        year = date.year
        week = date.isocalendar()[1]
        key = f'هفته {week}'
        weekly_data[key] += v
    sorted_weekly_data = sorted(weekly_data.items(), key=lambda item: int(re.findall(r'\d+', item[0])[0]))
    weekly_data = dict(sorted_weekly_data)
    weekly_data_output = {}
    for k, v in weekly_data.items():
        weekly_data_output[f"هفته {ascii_to_persian(re.findall(r'\d+', k)[0])}"] = v
    weeks = list(weekly_data_output.keys())
    values = list(weekly_data_output.values())
    return weeks, values
    
print(divide_weekly(x, y))



