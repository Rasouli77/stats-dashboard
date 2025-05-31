from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from datetime import datetime, date
from .models import PeopleCounting
from django.db.models import Sum
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .forms import Generate_User
import jdatetime
import json
from django.http import HttpResponseForbidden
from .camera_data import create_camera_data_record, get_custom_date_camera_data
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
    queryset = PeopleCounting.objects.values("date").annotate(total=Sum("entry")).order_by("date")
    branches = PeopleCounting.objects.values_list("branch", flat=True).distinct()
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
    content_type_PeopleCounting = ContentType.objects.get_for_model(PeopleCounting)
    permission_view_PeopleCounting = Permission.objects.get(
        codename="view_PeopleCounting",
        content_type=content_type_PeopleCounting,
    )
    permission_change_PeopleCounting = Permission.objects.get(
        codename="change_PeopleCounting",
        content_type=content_type_PeopleCounting,
    )
    permission_delete_PeopleCounting = Permission.objects.get(
        codename="delete_PeopleCounting",
        content_type=content_type_PeopleCounting,
    )
    permission_add_PeopleCounting = Permission.objects.get(
        codename="add_PeopleCounting",
        content_type=content_type_PeopleCounting,
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
    permission_to_add_PeopleCounting = request.GET.get("permission-to-add-PeopleCounting")
    if permission_to_add_PeopleCounting == "add_PeopleCounting":
        user.user_permissions.add(permission_add_PeopleCounting)
    
    permission_to_delete_PeopleCounting = request.GET.get("permission-to-delete-PeopleCounting")
    if permission_to_delete_PeopleCounting == "delete_PeopleCounting":
        user.user_permissions.add(permission_delete_PeopleCounting)

    permission_to_view_PeopleCounting = request.GET.get("permission-to-view-PeopleCounting")
    if permission_to_view_PeopleCounting == "view_PeopleCounting":
        user.user_permissions.add(permission_view_PeopleCounting)

    permission_to_change_PeopleCounting = request.GET.get("permission-to-change-PeopleCounting")
    if permission_to_change_PeopleCounting == "change_PeopleCounting":
        user.user_permissions.add(permission_change_PeopleCounting)
    
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

def test(request):
    x = get_custom_date_camera_data("172.16.20.103", "2025-05-01", "2025-05-05")
    print(x)
    create_camera_data_record(x)
    return HttpResponse("<p>test</p>")
