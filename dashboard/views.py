from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime, date
from .models import PeopleCounting, Branch, UserProfile, PermissionToViewBranch, Campaign
from django.db.models import Sum
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .forms import Generate_User, UserPermissions, AssignBranchPermissions, CreateCampaign
import jdatetime
import json
from django.http import HttpResponseForbidden
from django.contrib import messages
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
    
def convert_gregorian_to_jalali(g_date):
    """Convert a Gregorian date (datetime.date or datetime.datetime) to Jalali (YYYY-MM-DD)."""
    if not g_date:
        return ""
    j_date = jdatetime.date.fromgregorian(date=g_date)
    return j_date.strftime("%Y-%m-%d")

@login_required
def people_counter(request, url_hash):
    queryset = (
        PeopleCounting.objects.filter(merchant__url_hash=url_hash)
        .values("date")
        .annotate(total_entry=Sum("entry"))
        .annotate(total_exit=Sum("exit"))
        .order_by("date")
    )
    permissions = PermissionToViewBranch.objects.filter(user__pk=request.user.profile.pk)
    if len(permissions) == 0 and request.user.profile.is_manager != True:
        return render(request, "401.html", status=401)
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
    if request.user.profile.merchant.url_hash == url_hash and request.user.profile.is_manager == True and request.user.is_active == True:
        form = Generate_User(request.POST)
        if form.is_valid():
            new_user = form.save()
            try:
                UserProfile.objects.create(
                    user=new_user,
                    merchant=request.user.profile.merchant,
                    mobile="",
                    is_manager=False
                )
            except Exception as e:
                print(e)
        return render(request, "create-user.html", {"form": form})
    return render(request, "401.html", status=401)


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
def branch_permissions(request, user_id):
    user_profile = UserProfile.objects.get(user=user_id)
    perms = PermissionToViewBranch.objects.filter(user=user_profile)
    branches = Branch.objects.filter(merchant=user_profile.merchant)
    branch_count = branches.count()
    allowed_branches = []
    for perm in perms:
        allowed_branches.append(perm.branch.pk)
    if len(allowed_branches) > 0:
        branches = branches.exclude(pk__in=allowed_branches)
    if request.user.is_active == True and request.user.profile.is_manager == True and request.user.profile.merchant.url_hash == user_profile.merchant.url_hash:
        if request.method == "POST":
            form = AssignBranchPermissions(request.POST)
            if form.is_valid():
                form.save()
                return redirect("edit-branch-permissions", user_profile.user.pk)
        else:
            form = AssignBranchPermissions()
        return render(request, "branch-permissions.html", {"form": form, "user_profile_id": user_profile.pk, "perms": perms, "branches":branches, "branch_count": branch_count, "allowed_branch_count": len(allowed_branches)})
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
    if request.user.pk == user.pk and request.user.is_active==True:
        return render(request, "profile.html", {"user":user, "permissions": user_permissions, "branches": allowed_branches})
    
    if request.user.profile.merchant.url_hash == user.profile.merchant.url_hash and request.user.profile.is_manager == True and request.user.is_active==True:
        return render(request, "profile.html", {"user":user, "permissions": user_permissions, "branches": allowed_branches, "branch_length": len(allowed_branches)})

    return render(request, "401.html", status=401)

def test(request):
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
    return render(request, "landing.html")

@login_required
def campaign(request, url_hash):
    campaigns = Campaign.objects.filter(branch__merchant__url_hash=request.user.profile.merchant.url_hash).order_by("pk")
    permissions = PermissionToViewBranch.objects.filter(user__pk=request.user.profile.pk)
    permission_list = []
    for permission in permissions:
        permission_list.append(permission.branch.pk)
    branches = Branch.objects.filter(pk__in=permission_list).only("pk", "name")
    if request.user.profile.is_manager == False:
        campaigns = campaigns.filter(branch__pk__in=branches).order_by("pk")
    if request.user.profile.is_manager == True and request.user.is_active == True:
        return render(request, "campaign.html", {"campaigns": campaigns})
    return render(request, "401.html", status=401)

@login_required
def create_campaign(request, url_hash):
    if request.user.profile.merchant.url_hash == url_hash:
        permissions = PermissionToViewBranch.objects.filter(user__merchant__url_hash=url_hash, user__pk=request.user.profile.pk)
        permission_list = []
        for permission in permissions:
            permission_list.append(permission.branch.pk)
        branches = Branch.objects.filter(pk__in=permission_list).only("pk", "name")
        if request.user.profile.is_manager == True and request.user.is_active == True:
            branches = Branch.objects.filter(merchant__url_hash=url_hash).only("pk", "name")
        form = CreateCampaign(request.POST)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "کمپین با موفقیت ساخته شد")
            else:
                messages.error(request, "مشکلی در اطلاعات وارد شده وجود دارد")
        return render(request, "create-campaign.html", {"form": form, "branches": branches})
    return render(request, "401.html", status=401)

@login_required
def edit_campaign(request, campaign_id):
    campaign = Campaign.objects.get(pk=campaign_id)
    permissions = PermissionToViewBranch.objects.filter(user__pk=request.user.profile.pk)
    permission_list = []
    for permission in permissions:
        permission_list.append(permission.branch.pk)
    branches = Branch.objects.filter(pk__in=permission_list).only("pk", "name")
    if request.user.profile.is_manager == True:
        branches = Branch.objects.filter(merchant__url_hash=request.user.profile.merchant.url_hash) 
    if campaign.branch.pk in branches or request.user.profile.is_manager == True:
        form = 0
        if request.method == "POST":
            form = CreateCampaign(request.POST, instance=campaign)
            if form.is_valid():
                form.save()
                messages.success(request, "کمپین با موفقیت تغییر یافت")
            else:
                messages.error(request, "مشکلی در اطلاعات وارد شده وجود دارد")
        else:
            form = CreateCampaign(instance=campaign)
        jalali_start_date = convert_gregorian_to_jalali(campaign.start_date)
        jalali_end_date = convert_gregorian_to_jalali(campaign.end_date)
        return render(request, "edit-campaign.html", {"form": form, "campaign": campaign, "branches": branches, "jalali_start_date": jalali_start_date, "jalali_end_date": jalali_end_date})
    return render(request, "edit-campaign.html", {"branches": branches, "campaign": campaign})

@login_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    jalali_start_date = convert_gregorian_to_jalali(campaign.start_date)
    jalali_end_date = convert_gregorian_to_jalali(campaign.end_date)
    if request.method == "POST":
        campaign.delete()
        return redirect('campaign', request.user.profile.merchant.url_hash)
    return render(request, "delete-campaign.html", {"campaign": campaign, "jalali_start_date": jalali_start_date, "jalali_end_date": jalali_end_date})

def update_stats(request):
    pass
