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
from django.http import HttpResponseForbidden
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
    branches = Stats.objects.values_list("branch", flat=True).distinct()
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
    return render(request, "people-counter.html", {"dates": json.dumps(dates), "entry_totals": json.dumps(entry_totals), "branches": branches})

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

@login_required
def user_permissions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not request.user.is_staff:
        return HttpResponseForbidden("شما اجازه دسترسی به این قسمت را ندارید")
    if not request.user.is_active:
        return HttpResponseForbidden("شما اجازه دسترسی به این قسمت را ندارید")
    content_type_stats = ContentType.objects.get_for_model(Stats)
    permission_view_stats = Permission.objects.get(
        codename="view_stats",
        content_type=content_type_stats,
    )
    permission_change_stats = Permission.objects.get(
        codename="change_stats",
        content_type=content_type_stats,
    )
    permission_delete_stats = Permission.objects.get(
        codename="delete_stats",
        content_type=content_type_stats,
    )
    permission_add_stats = Permission.objects.get(
        codename="add_stats",
        content_type=content_type_stats,
    )
    content_type_user = ContentType.objects.get_for_model(User)
    permission_add_user = Permission.objects.get(
        codename="add_user",
        content_type=content_type_user,
    )
    permission_delete_user = Permission.objects.get(
        codename="delete_user",
        content_type=content_type_user,
    )
    permission_view_user = Permission.objects.get(
        codename="view_user",
        content_type=content_type_user,
    )
    permission_change_user = Permission.objects.get(
        codename="change_user",
        content_type=content_type_user,
    )
    permission_to_add_stats = request.GET.get("permission-to-add-stats")
    if permission_to_add_stats == "add_stats":
        user.user_permissions.add(permission_add_stats)
    
    permission_to_delete_stats = request.GET.get("permission-to-delete-stats")
    if permission_to_delete_stats == "delete_stats":
        user.user_permissions.add(permission_delete_stats)

    permission_to_view_stats = request.GET.get("permission-to-view-stats")
    if permission_to_view_stats == "view_stats":
        user.user_permissions.add(permission_view_stats)

    permission_to_change_stats = request.GET.get("permission-to-change-stats")
    if permission_to_change_stats == "change_stats":
        user.user_permissions.add(permission_change_stats)
    
    permission_to_add_user = request.GET.get("permission-to-add-user")
    if permission_to_add_user == "add_user":
        user.user_permissions.add(permission_add_user) 
    
    permission_to_delete_user = request.GET.get("permission-to-delete-user")
    if permission_to_delete_user == "delete_user":
        user.user_permissions.add(permission_delete_user)

    permission_to_view_user = request.GET.get("permission-to-view-user")
    if permission_to_view_user == "view_user":
        user.user_permissions.add(permission_view_user)

    permission_to_change_user = request.GET.get("permission-to-change-user")
    if permission_to_change_user == "change_user":
        user.user_permissions.add(permission_change_user)

    
    return render(request, "user-permissions.html", {"user":user})

def calender(request):
    return render(request, "calendar.html")

