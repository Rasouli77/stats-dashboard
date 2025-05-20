from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, date
from .models import Stats
from django.db.models import Sum
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .forms import Generate_User
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

@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, "users.html", {"users":users})

@login_required
def generate_user(request):
    form = Generate_User(request.POST)
    if form.is_valid():
        form.save()
    return render(request, "create-user.html", {"form": form})

def user_permissions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    content_type = ContentType.objects.get_for_model(Stats)
    permission_view_stats = Permission.objects.get(
        codename="view_stats",
        content_type=content_type,
    )
    permission_change_stats = Permission.objects.get(
        codename="change_stats",
        content_type=content_type,
    )
    permission_delete_stats = Permission.objects.get(
        codename="delete_stats",
        content_type=content_type,
    )
    permission_add_stats = Permission.objects.get(
        codename="add_stats",
        content_type=content_type,
    )
    permission = request.GET.get("permission")
    if permission == "add":
        user.user_permissions.add(permission_add_stats)
    
    if permission == "delete":
        user.user_permissions.add(permission_delete_stats)

    if permission == "view":
        user.user_permissions.add(permission_view_stats)

    if permission == "change":
        user.user_permissions.add(permission_change_stats)
    return render(request, "user-permissions.html", {"user":user})

def calender(request):
    return render(request, "calendar.html")

