from django.shortcuts import render
from datetime import datetime, date
from .models import Stats
from django.db.models import Sum
import jdatetime
import json
# Create your views here.

def jalali_to_gregorian(date_str: str):
    try:
        jyear, jmonth, jday = map(int, date_str.split("-"))
        gregorian_date = jdatetime.date(jyear, jmonth, jday).togregorian()
        return gregorian_date
    except Exception as e:
        print(e)
        return None

def people_counter(request):
    queryset = Stats.objects.values("date").annotate(total=Sum("entry")).order_by("date")
    branch = request.GET.get("branch")
    start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
    end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
    start_date = 0
    end_date = 0
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            queryset = queryset.filter(date__range=(start_date, end_date))
        except Exception as e:
            print(e)
    
    if branch:
        try:
            queryset = queryset.filter(branch=branch)
        except Exception as e:
            print(e)
    dates = [str(row["date"].strftime("%Y-%m-%d")) for row in queryset]
    entry_totals = [float(row["total"]) for row in queryset]
    return render(request, "people-counter.html", {"dates": json.dumps(dates), "entry_totals": json.dumps(entry_totals)})


