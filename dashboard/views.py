from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime, date
from .models import PeopleCounting, Branch, UserProfile, PermissionToViewBranch
from django.db.models import Sum
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .forms import Generate_User, UserPermissions
import jdatetime
import json
from django.http import HttpResponseForbidden
from django.db.models import F
from collections import defaultdict
from .camera_data import get_custom_date_camera_data, update_or_create_camera_data
from django.db import connection

# Create your views here.


def jalali_to_gregorian(date_str: str):
    try:
        jyear, jmonth, jday = map(int, date_str.split("-"))
        gregorian_date = jdatetime.date(jyear, jmonth, jday).togregorian()
        return gregorian_date
    except Exception as e:
        print(e)
        return None

@login_required
def people_counter(request, url_hash):
    queryset = (
        PeopleCounting.objects.filter(merchant__url_hash=url_hash)
        .values("date")
        .annotate(total_entry=Sum("entry"))
        .annotate(total_exit=Sum("exit"))
        .order_by("date")
    )
    if request.user.profile.is_manager == True:
        branches = Branch.objects.filter(merchant__url_hash=url_hash).only("name", "pk")
    else:
        permitted_branches = PermissionToViewBranch.objects.filter(
            user__merchant__url_hash=url_hash, user__pk=request.user.profile.pk
        )
        permitted_branches_list = []
        for permitted_branch in permitted_branches:
            permitted_branches_list.append(permitted_branch.branch.pk)
        branches = Branch.objects.filter(
            merchant__url_hash=url_hash, pk__in=permitted_branches_list
        ).only("name", "pk")

    selected_branches = request.GET.getlist("branch")
    start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
    end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
    start_date = 0
    end_date = 0
    branch_count = branches.count()
    entry_totals = []
    exit_totals = []
    branches_stats = {}
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            queryset = queryset.filter(date__range=(start_date, end_date))
        except Exception as e:
            print(e)

    # If there is one branch
    if len(selected_branches) == 1:
        try:
            queryset = queryset.filter(branch=selected_branches[0])
            entry_totals = [float(row["total_entry"]) for row in queryset]
            exit_totals = [float(row["total_exit"]) for row in queryset]
        except Exception as e:
            print(e)

    # If there is more than one branch
    if len(selected_branches) > 1 and len(selected_branches) < branch_count:
        branches_stats = defaultdict(lambda: {"date": [], "entry_totals": []})
        try:
            queryset = queryset.filter(branch__in=selected_branches)
            for row in queryset:
                branches_stats["date"].append(row["date"].strftime("%Y-%m-%d"))
                branches_stats["entry_totals"].append(float(row["total_entry"]))
        except Exception as e:
            print(e)

    entry_totals = [float(row["total_entry"]) for row in queryset]
    exit_totals = [float(row["total_exit"]) for row in queryset]
    dates = [str(row["date"].strftime("%Y-%m-%d")) for row in queryset]
    # After your view or queryset logic
    print("Total queries executed:", len(connection.queries))

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(
            {
                "dates": dates,
                "entry_totals": entry_totals,
                "exit_totals": exit_totals,
            }
        )
    return render(
        request,
        "people-counter.html",
        {
            "dates": json.dumps(dates),
            "entry_totals": json.dumps(entry_totals),
            "exit_totals": json.dumps(exit_totals),
            "branches": branches,
            "branches_data": json.dumps(dict(branches_stats)),
        },
    )


@login_required
def users_list(request, url_hash):
    users = UserProfile.objects.filter(merchant__url_hash=url_hash)
    if request.user.profile.merchant.url_hash == url_hash and request.user.profile.is_manager == True and request.user.is_active == True:
        return render(request, "users.html", {"users": users})
    return render(request, "401.html", status=401)

@login_required
def generate_user(request, url_hash):
    form = Generate_User(request.POST)
    if form.is_valid():
        form.save()
    return render(request, "create-user.html", {"form": form})


@login_required
def user_permissions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.profile.merchant.url_hash == user.profile.merchant.url_hash and request.user.is_active == True and request.user.profile.is_manager == True:
        if request.method == "POST":
            form = UserPermissions(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect("profile", user.pk)
        else:
            form = UserPermissions(instance=user)
        return render(request, "user-permissions.html", {"user": user, "form": form})
    return render(request, "401.html", status=401)
    

@login_required
def calender(request, url_hash):
    return render(request, "calendar.html")

@login_required
def home(request, url_hash):
    return render(request, "home.html")

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_permissions = user.user_permissions.all()
    user_profile = UserProfile.objects.get(user=user.pk)
    allowed_branches = PermissionToViewBranch.objects.filter(user=user_profile.pk)
    print(allowed_branches)
    print(user_permissions)
    if request.user.pk == user.pk and request.user.is_active==True:
        return render(request, "profile.html", {"user":user, "permissions": user_permissions, "branches": allowed_branches})
    
    if request.user.profile.merchant.url_hash == user.profile.merchant.url_hash and request.user.profile.is_manager == True and request.user.is_active==True:
        return render(request, "profile.html", {"user":user, "permissions": user_permissions, "branches": allowed_branches})

    
    return render(request, "401.html", status=401)


def test(self):
    # aghdasieh = get_custom_date_camera_data("172.16.20.103", "2025-05-31", "2025-06-06")
    # iranmallone = get_custom_date_camera_data("172.16.70.75", "2025-05-31", "2025-06-06")
    # iranmalltwo = get_custom_date_camera_data("172.16.70.128", "2025-05-31", "2025-06-06")
    # mehrad = get_custom_date_camera_data("172.16.90.241", "2025-05-31", "2025-06-06")
    # hadish_one = get_custom_date_camera_data("172.16.40.174", "2025-05-31", "2025-06-06")
    # hadish_two = get_custom_date_camera_data("172.16.40.175", "2025-05-31", "2025-06-06")
    # update_or_create_camera_data(aghdasieh, 1, 1, 1)
    # update_or_create_camera_data(iranmallone, 5, 1, 4)
    # update_or_create_camera_data(iranmalltwo, 6, 1, 4)
    # update_or_create_camera_data(mehrad, 2, 1, 2)
    # update_or_create_camera_data(hadish_one, 3, 1, 3)
    # update_or_create_camera_data(hadish_two, 4, 1, 3)
    pass
