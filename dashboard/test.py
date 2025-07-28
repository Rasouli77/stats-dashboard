import jdatetime
import datetime
import openpyxl

def get_dates(start_date_str: str, end_date_str:str):
    date_list = []
    start_date = jdatetime.datetime.strptime(start_date_str, "%Y-%m-%d").date().togregorian()
    end_date = jdatetime.datetime.strptime(end_date_str, "%Y-%m-%d").date().togregorian()
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=1)
    date_list = [jdatetime.datetime.fromgregorian(date=date).date().strftime("%Y-%m-%d") for date in date_list]

    return date_list

x = get_dates("1404-05-01", "1404-05-10")
print(x)

def create_excel_template(start_date: str, end_date: str, branch_list: list, filename="222222.xlsx", jalali_date=False):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "تمپلیت آپلود اطلاعات فروش شعب"
    ws.append(["تاریخ", "کد شعبه", "مبلغ فاکتور", "تعداد فاکتور"])
    branches = branch_list
    dates = get_dates(start_date, end_date)
    for branch in branches:
        for date in dates:
            ws.append([date, branch, "", ""])
    wb.save(filename)
