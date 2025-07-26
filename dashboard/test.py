import jdatetime
import datetime

x = "1394-03-02"
b = x[:2]
if b == "13" or b == "14":
    year, month, day = map(int, x.split("-"))
    print(year, month, day)
    x_jalali_date = jdatetime.date(year, month, day)
    print(x_jalali_date)
    x_gregorian_date = x_jalali_date.togregorian()
    print(x_gregorian_date, type(x_gregorian_date))
else:
    x_gregorian_date = datetime.datetime.strptime(x, "%Y-%m-%d").date()
    print(x_gregorian_date, type(x_gregorian_date))

