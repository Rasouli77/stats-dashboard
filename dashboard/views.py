from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from datetime import datetime, date, timedelta

import openpyxl.styles
from .models import (
    PeopleCounting,
    Branch,
    UserProfile,
    PermissionToViewBranch,
    Campaign,
    Cam,
    Invoice,
)
from django.db.models import Sum, F
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .forms import (
    Generate_User,
    UserPermissions,
    AssignBranchPermissions,
    CreateCampaign,
    UploadInvoiceExcel,
    InvoiceForm,
)
import jdatetime
import json
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import F
from collections import defaultdict
from .camera_data import get_custom_date_camera_data, update_or_create_camera_data
from django.db import connection
from django.utils import timezone
import subprocess
import openpyxl
from io import BytesIO
import random


def perm_to_open(request, url_hash):
    """Checks if the user has the right to open the page."""
    if not request.user.is_active:
        return False
    merchant = request.user.profile.merchant
    try:
        if merchant.url_hash:
            if merchant.url_hash != url_hash:
                return False
            else:
                return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def jalali_to_gregorian(date_str: str):
    """Convert a Jalali date (datetime.date or datetime.datetime) to Gregorian (YYYY-MM-DD)."""
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
    """This provides an overview for people counters in all branches."""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    queryset = (
        PeopleCounting.objects.filter(merchant__url_hash=url_hash)
        .values("date")
        .annotate(total_entry=Sum("entry"))
        .annotate(total_exit=Sum("exit"))
        .order_by("date")
    )
    permissions = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user__pk=request.user.profile.pk)
    )
    if len(permissions) == 0 and not request.user.profile.is_manager:
        return render(request, "401.html", status=401)
    if request.user.profile.is_manager:
        branches = Branch.objects.only("name", "pk").filter(merchant__url_hash=url_hash)
        campaigns = Campaign.objects.defer("date_created", "last_modified").filter(branch__merchant__url_hash=url_hash)
    else:
        permitted_branches = (
            PermissionToViewBranch.objects.defer("date_created", "last_modified")
            .select_related("branch")
            .filter(user__pk=request.user.profile.pk)
        )
        permitted_branches_list = []
        for permitted_branch in permitted_branches:
            permitted_branches_list.append(permitted_branch.branch.pk)
        branches = Branch.objects.only("name", "pk").filter(
            merchant__url_hash=url_hash, pk__in=permitted_branches_list
        )
        campaigns = Campaign.objects.defer("date_created", "last_modified").filter(branch__merchant__url_hash=url_hash, branch__pk__in=permitted_branches_list)
        queryset = queryset.filter(branch__pk__in=permitted_branches_list)
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
            "campaigns": campaigns
        },
    )


@login_required
def users_list(request, url_hash):
    """A list of all users for managers."""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    users = UserProfile.objects.filter(merchant__url_hash=url_hash)
    if (
        request.user.profile.merchant.url_hash == url_hash
        and request.user.profile.is_manager
        and request.user.is_active
    ):
        print("Total queries executed:", connection.queries, len(connection.queries))
        return render(request, "users.html", {"users": users})
    return render(request, "401.html", status=401)


@login_required
def generate_user(request, url_hash):
    """Using this, managers can create users."""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    if (
        request.user.profile.merchant.url_hash == url_hash
        and request.user.profile.is_manager
        and request.user.is_active
    ):
        form = Generate_User(request.POST)
        if form.is_valid():
            new_user = form.save()
            try:
                UserProfile.objects.create(
                    user=new_user,
                    merchant=request.user.profile.merchant,
                    mobile="",
                    is_manager=False,
                )
            except Exception as e:
                print(e)
        print("Total queries executed:", connection.queries, len(connection.queries))
        return render(request, "create-user.html", {"form": form})
    return render(request, "401.html", status=401)


@login_required
def user_permissions(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if (
        request.user.profile.merchant.url_hash == user.profile.merchant.url_hash
        and request.user.is_active
        and request.user.profile.is_manager
    ):
        if request.method == "POST":
            form = UserPermissions(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect("profile", user.pk)
        else:
            form = UserPermissions(instance=user)
        print("Total queries executed:", connection.queries, len(connection.queries))
        return render(request, "user-permissions.html", {"user": user, "form": form})
    return render(request, "401.html", status=401)


@login_required
def branch_permissions(request, user_id):
    user_profile = UserProfile.objects.get(user=user_id)
    perms = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user=user_profile)
    )
    branches = Branch.objects.defer(
        "country", "province", "city", "district", "date_created", "last_modified"
    ).filter(merchant=user_profile.merchant)
    branch_count = branches.count()
    allowed_branches = []
    for perm in perms:
        allowed_branches.append(perm.branch.pk)
    if len(allowed_branches) > 0:
        branches = branches.exclude(pk__in=allowed_branches)
    if (
        request.user.is_active
        and request.user.profile.is_manager
        and request.user.profile.merchant.url_hash == user_profile.merchant.url_hash
    ):
        if request.method == "POST":
            form = AssignBranchPermissions(request.POST)
            if form.is_valid():
                form.save()
                return redirect("edit-branch-permissions", user_profile.user.pk)
        else:
            form = AssignBranchPermissions()
        return render(
            request,
            "branch-permissions.html",
            {
                "form": form,
                "user_profile_id": user_profile.pk,
                "perms": perms,
                "branches": branches,
                "branch_count": branch_count,
                "allowed_branch_count": len(allowed_branches),
            },
        )
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(request, "401.html", status=401)


@login_required
def home(request, url_hash):
    """A general overview of certain aggregations"""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    queryset = PeopleCounting.objects.defer(
        "date_created", "last_modified", "exit"
    ).filter(merchant__url_hash=url_hash)
    # 7 days
    today = timezone.now().today()
    last_7_days_start = today - timedelta(days=7)
    last_7_days_end = today
    previous_7_days_start = today - timedelta(days=14)
    previous_7_days_end = today - timedelta(days=7)

    # entries
    last_7_days_entry = queryset.filter(
        date__range=(last_7_days_start, last_7_days_end)
    ).aggregate(total_entry=Sum("entry"))
    previous_7_days_entry = queryset.filter(
        date__range=(previous_7_days_start, previous_7_days_end)
    ).aggregate(total_entry=Sum("entry"))
    try:
        diff_7_per = (
            (last_7_days_entry["total_entry"] - previous_7_days_entry["total_entry"])
            / previous_7_days_entry["total_entry"]
        ) * 100
    except Exception as e:
        print(e)
        diff_7_per = 0
    try:
        rounded_diff_7_per = round(diff_7_per, 2)
    except Exception as e:
        print(e)
        rounded_diff_7_per = 0

    # branches
    last_7_days_best_branch_name = (
        queryset.filter(date__range=(last_7_days_start, last_7_days_end))
        .values("branch__id", "branch__name")
        .annotate(total_entry=Sum("entry"))
        .order_by("-total_entry")
        .first()
    )
    last_7_days_worst_branch_name = (
        queryset.filter(date__range=(last_7_days_start, last_7_days_end))
        .values("branch__id", "branch__name")
        .annotate(total_entry=Sum("entry"))
        .order_by("total_entry")
        .first()
    )

    # branch rank
    branch_7_day_ranks = (
        queryset.filter(date__range=(last_7_days_start, last_7_days_end))
        .values("branch__id", "branch__name")
        .annotate(total_entry=Sum("entry"))
        .annotate(percent_seven=(Sum("entry") / last_7_days_entry["total_entry"]) * 100)
        .order_by("-total_entry")
    )

    # 30 days
    last_30_days_start = today - timedelta(days=30)
    last_30_days_end = today
    previous_30_days_start = today - timedelta(days=60)
    previous_30_days_end = today - timedelta(days=30)

    # entries
    last_30_days_entry = queryset.filter(
        date__range=(last_30_days_start, last_30_days_end)
    ).aggregate(total_entry=Sum("entry"))
    previous_30_days_entry = queryset.filter(
        date__range=(previous_30_days_start, previous_30_days_end)
    ).aggregate(total_entry=Sum("entry"))
    try:
        diff_30_per = (
            (last_30_days_entry["total_entry"] - previous_30_days_entry["total_entry"])
            / previous_30_days_entry["total_entry"]
        ) * 100
    except Exception as e:
        print(e)
        diff_30_per = 0
    try:
        rounded_diff_30_per = round(diff_30_per, 2)
    except Exception as e:
        print(e)
        rounded_diff_30_per = 0

    # branches
    last_30_days_best_branch_name = (
        queryset.filter(date__range=(last_30_days_start, last_30_days_end))
        .values("branch__id", "branch__name")
        .annotate(total_entry=Sum("entry"))
        .order_by("-total_entry")
        .first()
    )
    last_30_days_worst_branch_name = (
        queryset.filter(date__range=(last_30_days_start, last_30_days_end))
        .values("branch__id", "branch__name")
        .annotate(total_entry=Sum("entry"))
        .order_by("total_entry")
        .first()
    )

    # branch rank
    branch_30_day_ranks = (
        queryset.filter(date__range=(last_30_days_start, last_30_days_end))
        .values("branch__id", "branch__name")
        .annotate(total_entry=Sum("entry"))
        .annotate(
            percent_thirty=(Sum("entry") / last_30_days_entry["total_entry"]) * 100
        )
        .order_by("-total_entry")
    )
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(
        request,
        "home.html",
        {
            "last_7_days_best_branch_name": last_7_days_best_branch_name,
            "last_7_days_worst_branch_name": last_7_days_worst_branch_name,
            "branch_30_day_ranks": branch_30_day_ranks,
            "branch_7_day_ranks": branch_7_day_ranks,
            "last_30_days_best_branch_name": last_30_days_best_branch_name,
            "last_30_days_worst_branch_name": last_30_days_worst_branch_name,
            "rounded_diff_30_per": rounded_diff_30_per,
            "rounded_diff_7_per": rounded_diff_7_per,
            "last_30_days_entry_total": last_30_days_entry["total_entry"],
            "last_7_days_entry_total": last_7_days_entry["total_entry"],
            "previous_7_days_entry_total": previous_7_days_entry["total_entry"],
            "previous_30_days_entry_total": previous_30_days_entry["total_entry"],
        },
    )


@login_required
def profile(request, user_id):
    """This loads a profile for each user."""
    user = get_object_or_404(User, pk=user_id)
    user_permissions = user.user_permissions.all()
    user_profile = UserProfile.objects.get(user=user.pk)
    allowed_branches = PermissionToViewBranch.objects.defer(
        "date_created", "last_modified"
    ).filter(user=user_profile.pk)
    if request.user.pk == user.pk and request.user.is_active:
        print("Total queries executed:", connection.queries, len(connection.queries))
        return render(
            request,
            "profile.html",
            {
                "user": user,
                "permissions": user_permissions,
                "branches": allowed_branches,
            },
        )

    if (
        request.user.profile.merchant.url_hash == user.profile.merchant.url_hash
        and request.user.profile.is_manager
        and request.user.is_active
    ):
        return render(
            request,
            "profile.html",
            {
                "user": user,
                "permissions": user_permissions,
                "branches": allowed_branches,
                "branch_length": len(allowed_branches),
            },
        )
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(request, "401.html", status=401)


def ping_ip(ip, timeout=15):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 2,  # Overall timeout to avoid hanging
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timeout: Ping to {ip} took too long.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def test(request):
    today = timezone.now().date()
    raw_yesterday = today - timedelta(days=1)
    yesterday = raw_yesterday.strftime("%Y-%m-%d")
    cams = Cam.objects.select_related("merchant", "branch").all()
    ips = []
    for cam in cams:
        ips.append(
            {
                "ip": cam.ip,
                "cam_id": cam.pk,
                "merchant_id": cam.merchant.pk,
                "branch_id": cam.branch.pk,
            }
        )
    print(ips)
    for ip in ips:
        print(ip)
        if ping_ip(ip["ip"]):
            print(ip["ip"])
            try:
                data = get_custom_date_camera_data(ip["ip"], yesterday, yesterday)
                update_or_create_camera_data(
                    data, ip["cam_id"], ip["merchant_id"], ip["branch_id"]
                )
            except Exception as e:
                print(e)
        else:
            print(f"This ip has a problem: {ip['ip']}")
    return render(request, "landing.html")


@login_required
def campaign(request, url_hash):
    """A full list of campaigns if allowed"""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    campaigns = Campaign.objects.filter(
        branch__merchant__url_hash=request.user.profile.merchant.url_hash
    ).order_by("pk")
    permissions = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user__pk=request.user.profile.pk)
    )
    permission_list = []
    for permission in permissions:
        permission_list.append(permission.branch.pk)
    branches = Branch.objects.defer(
        "country", "province", "city", "district", "date_created", "last_modified"
    ).filter(merchant__url_hash=url_hash, pk__in=permission_list)
    if not request.user.profile.is_manager:
        campaigns = campaigns.filter(branch__pk__in=branches).order_by("pk")
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(request, "campaign.html", {"campaigns": campaigns})


@login_required
def create_campaign(request, url_hash):
    """Using this, users can create campaigns."""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    if request.user.profile.merchant.url_hash == url_hash:
        permissions = (
            PermissionToViewBranch.objects.defer("date_created", "last_modified")
            .select_related("branch")
            .filter(user__pk=request.user.profile.pk)
        )
        permission_list = []
        for permission in permissions:
            permission_list.append(permission.branch.pk)
        branches = Branch.objects.defer(
            "country", "province", "city", "district", "date_created", "last_modified"
        ).filter(merchant__url_hash=url_hash, pk__in=permission_list)
        if request.user.profile.is_manager and request.user.is_active:
            branches = Branch.objects.defer(
                "country",
                "province",
                "city",
                "district",
                "date_created",
                "last_modified",
            ).filter(merchant__url_hash=url_hash)
        form = CreateCampaign(request.POST)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "کمپین با موفقیت ساخته شد")
            else:
                messages.error(request, "مشکلی در اطلاعات وارد شده وجود دارد")
        return render(
            request, "create-campaign.html", {"form": form, "branches": branches}
        )
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(request, "401.html", status=401)


@login_required
def edit_campaign(request, campaign_id):
    """This edits each campaign using a form if permitted."""
    campaign = Campaign.objects.get(pk=campaign_id)
    permissions = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user__pk=request.user.profile.pk)
    )
    permission_list = []
    for permission in permissions:
        permission_list.append(permission.branch.pk)
    branches = Branch.objects.defer(
        "country", "province", "city", "district", "date_created", "last_modified"
    ).filter(pk__in=permission_list)
    if request.user.profile.is_manager:
        branches = Branch.objects.defer(
            "country", "province", "city", "district", "date_created", "last_modified"
        ).filter(merchant__url_hash=request.user.profile.merchant.url_hash)
    if campaign.branch.pk in branches or request.user.profile.is_manager:
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
        return render(
            request,
            "edit-campaign.html",
            {
                "form": form,
                "campaign": campaign,
                "branches": branches,
                "jalali_start_date": jalali_start_date,
                "jalali_end_date": jalali_end_date,
            },
        )
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(
        request, "edit-campaign.html", {"branches": branches, "campaign": campaign}
    )


@login_required
def delete_campaign(request, campaign_id):
    """This deletes each campaign by its id."""
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    jalali_start_date = convert_gregorian_to_jalali(campaign.start_date)
    jalali_end_date = convert_gregorian_to_jalali(campaign.end_date)
    if request.method == "POST":
        campaign.delete()
        return redirect("campaign", request.user.profile.merchant.url_hash)
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(
        request,
        "delete-campaign.html",
        {
            "campaign": campaign,
            "jalali_start_date": jalali_start_date,
            "jalali_end_date": jalali_end_date,
        },
    )


@login_required
def upload_excel_file_invoice(request, url_hash):
    """This uploads an excel file to create invoice objects accordingly."""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    if not request.user.has_perm("dashboard.add_invoice"):
        return render(request, "401.html", status=401)
    if not request.user.has_perm("dashboard.delete_invoice"):
        return render(request, "401.html", status=401)
    try:
        branches = Branch.objects.defer(
            "country", "province", "city", "district", "date_created", "last_modified"
        ).filter(merchant__url_hash=url_hash)
    except Exception:
        messages.error(request, "مرچنتی با این مشخصات یافت نشد.")
        return render(request, "upload_excel_invoice.html", {"error": f"{e}"})
    allowed_branches = []
    for branch in branches:
        allowed_branches.append(branch.pk)
    if request.method == "POST":
        form = UploadInvoiceExcel(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES["excel_file"]
            try:
                wb = openpyxl.load_workbook(excel_file)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    date, branch, total_amount, total_items = row[:2] + row[3:]
                    if isinstance(date, str):
                        if date:
                            first_two = date[:2]
                            if first_two == "13" or first_two == "14":
                                year, month, day = map(int, date.split("-"))
                                jalali_date = jdatetime.date(year, month, day)
                                date = jalali_date.togregorian()
                            else:
                                date = datetime.strptime(date, "%Y-%m-%d").date()
                    if branch and total_amount and total_items:
                        if int(branch) not in allowed_branches:
                            messages.warning(
                                request,
                                "یک یا چند ردیف دارای کد شعبی هستند که برای شما تعریف نشده است.",
                            )
                            return render(
                                request,
                                "upload_excel_invoice.html",
                                {
                                    "error": "از کد های زیر برای شعبه استفاده نمایید:",
                                    "branches": branches,
                                },
                            )
                        branch = branches.get(pk=int(branch))
                        Invoice.objects.update_or_create(
                            date=date,
                            branch=branch,
                            total_amount=str(int(total_amount)),
                            total_items=str(int(total_items)),
                        )
                messages.success(request, "اطلاعات فروش با موفقیت آپلود شدند")
                return redirect(reverse("upload_excel_file_invoice", args=[url_hash]))
            except Exception as e:
                messages.error(
                    request,
                    "فایل مورد نظر یافت نشد. فرمت فایل و نام فایل آپلود شده را دوباره بررسی فرمایید. فایل مورد نظر باید طبق نمونه تمپلیت آپلود شود.",
                )
                return render(request, "upload_excel_invoice.html", {"error": f"{e}"})
        else:
            messages.error(request, "فایل مورد نظر باید دارای فرمت اکسل باشد.")
            return render(
                request, "upload_excel_invoice.html", {"error": f"{form.errors}"}
            )
    else:
        form = UploadInvoiceExcel()
        print("Total queries executed:", connection.queries, len(connection.queries))
        return render(request, "upload_excel_invoice.html", {"form": form})


@login_required
def invoices(request, url_hash):
    """This shows a list of all invoices. Filtering is also enabled."""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    if not request.user.has_perm("dashboard.add_invoice"):
        return render(request, "401.html", status=401)
    branches = Branch.objects.defer(
        "country", "province", "city", "district", "date_created", "last_modified"
    ).filter(merchant__url_hash=url_hash)
    permissions = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user__pk=request.user.profile.pk)
    )
    permission_branch_keys = []
    for permission in permissions:
        permission_branch_keys.append(permission.branch.pk)
    allowed_branches = []
    if request.user.profile.is_manager:
        for branch in branches:
            allowed_branches.append(branch.pk)
    if not request.user.profile.is_manager and request.user.has_perm(
        "dashboard.add_invoice"
    ):
        allowed_branches = permission_branch_keys

    invoices = []
    branches = branches.filter(pk__in=allowed_branches)
    start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
    end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
    selected_branch_str = request.GET.getlist("branch")
    selected_branch = [int(item) for item in selected_branch_str]
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        if start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                if len(selected_branch) == 0:
                    invoices = (
                        Invoice.objects.filter(branch__pk__in=allowed_branches)
                        .filter(date__range=(start_date, end_date))
                        .annotate(branch_name=F("branch__name"))
                    )
                else:
                    invoices = (
                        Invoice.objects.filter(branch__pk__in=selected_branch)
                        .filter(date__range=(start_date, end_date))
                        .annotate(branch_name=F("branch__name"))
                    )
            except Exception as e:
                print(e)
            return JsonResponse({"invoices": list(invoices.values())})
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(
        request, "invoices.html", {"invoices": invoices, "branches": branches}
    )


@login_required
def invoice_detail(request, invoice_pk):
    """This shows the detail of each invoice record. You can also delete and edit the total amount as well as the item numbers."""
    invoice = (
        Invoice.objects.defer("date_created", "last_modified", "branch__date_created")
        .select_related("branch")
        .get(pk=invoice_pk)
    )
    permissions = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user__pk=request.user.profile.pk)
    )
    allowed_branches = []
    for permission in permissions:
        allowed_branches.append(permission.branch.pk)
    if not request.user.profile.is_manager:
        if invoice.branch.pk not in allowed_branches:
            return render(request, "401.html", status=401)
    form = InvoiceForm(instance=invoice)
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, "تغییرات با موفقیت اعمال شد")
            return redirect(reverse("invoice_detail", args=[invoice_pk]))
        else:
            messages.error(request, f"{form.errors}")
            return redirect(reverse("invoice_detail", args=[invoice_pk]))
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(request, "invoice_detail.html", {"invoice": invoice, "form": form})


@login_required
def invoice_delete(request, invoice_pk):
    """This deletes the said invoice."""
    invoice = (
        Invoice.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .get(pk=invoice_pk)
    )
    permissions = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user__pk=request.user.profile.pk)
    )
    url_hash = request.user.profile.merchant.url_hash
    allowed_branches = []
    for permission in permissions:
        allowed_branches.append(permission.branch.pk)
    if not request.user.profile.is_manager:
        if invoice.branch.pk not in allowed_branches:
            return render(request, "401.html", status=401)
    invoice.delete()
    return redirect(reverse("invoices", args=[url_hash]))


def get_dates(start_date_str: str, end_date_str: str):
    """This creates a Python list within the Jalali specificed time period."""
    date_list = []
    start_date = (
        jdatetime.datetime.strptime(start_date_str, "%Y-%m-%d").date().togregorian()
    )
    end_date = (
        jdatetime.datetime.strptime(end_date_str, "%Y-%m-%d").date().togregorian()
    )
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    date_list = [
        jdatetime.datetime.fromgregorian(date=date).date().strftime("%Y-%m-%d")
        for date in date_list
    ]
    return date_list


def create_excel_template(start_date: str, end_date: str, branch_list: dict):
    """It creates an excel file and styles it using Jalali start and end dates and a dictionary of numbers as keys and strings as values."""
    wb = openpyxl.Workbook()
    colors = [
        "FFF4CCCC",
        "FFFCE5CD",
        "FFFFF2CC",
        "FFD9EAD3",
        "FFD0E0E3",
        "FFCFE2F3",
        "FFD9D2E9",
        "FFEAD1DC",
        "FFEEEEEE",
        "FFBCBCBC",
    ]
    color_mapper = {}
    for item in branch_list.keys():
        color_mapper[item] = random.sample(colors, 1)[0]
    ws = wb.active
    ws.title = "تمپلیت آپلود اطلاعات فروش شعب"
    ws.append(["تاریخ", "کد شعبه", "نام شعبه", "مبلغ فاکتور", "تعداد فاکتور"])
    branches = branch_list
    dates = get_dates(start_date, end_date)
    for branch_id, branch_name in branches.items():
        for date in dates:
            ws.append([date, branch_id, branch_name, "", ""])

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        if row[1].value in color_mapper.keys():
            for cell in row:
                cell.fill = openpyxl.styles.PatternFill(
                    start_color=color_mapper[row[1].value],
                    end_color=color_mapper[row[1].value],
                    fill_type="solid",
                )
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output


@login_required
def excel_template_generator(request, url_hash):
    """This creates an excel template file for uploading to the system without any errors."""
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    permissions = (
        PermissionToViewBranch.objects.defer("date_created", "last_modified")
        .select_related("branch")
        .filter(user__pk=request.user.profile.pk)
    )
    allowed_branches = []
    if not request.user.profile.is_manager:
        for permission in permissions:
            allowed_branches.append(permission.branch.pk)
        branches = (
            Branch.objects.defer(
                "country",
                "province",
                "city",
                "district",
                "date_created",
                "last_modified",
            )
            .filter(merchant__url_hash=url_hash)
            .filter(pk__in=allowed_branches)
        )
    else:
        branches = Branch.objects.defer(
            "country", "province", "city", "district", "date_created", "last_modified"
        ).filter(merchant__url_hash=url_hash)
    try:
        start_date_str = str(request.GET.get("start-date"))
        end_date_str = str(request.GET.get("end-date"))
        branches_str = request.GET.getlist("branch")
        branches_int = [int(i) for i in branches_str]
        branch_dict = {}
        for branch in branches:
            if branch.pk in branches_int:
                branch_dict[branch.pk] = branch.name
        if start_date_str and end_date_str:
            excel_file = create_excel_template(
                start_date_str, end_date_str, branch_dict
            )
            response = HttpResponse(
                excel_file,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = f'attachment; filename="template.xlsx"'
            return response
    except Exception as e:
        print(e)
    print("Total queries executed:", connection.queries, len(connection.queries))
    return render(request, "create-excel-template.html", {"branches": branches})


@login_required
def invoice_counter(request, url_hash):
    # Rights
    if not perm_to_open(request, url_hash):
        return render(request, "401.html", status=401)
    # Permissions
    allowed_branches = []
    profile = request.user.profile
    all_branches = Branch.objects.defer(
            "country", "province", "city", "district", "date_created", "last_modified"
    ).filter(merchant__url_hash=url_hash)
    if not profile.is_manager:
        permissions = (
            PermissionToViewBranch.objects.defer("date_created", "last_modified")
            .select_related("branch")
            .filter(user__pk=profile.pk)
        )
        for permission in permissions:
            allowed_branches.append(permission.branch.pk)
    else:
        for item in all_branches:
            allowed_branches.append(item.pk)
    try:
        start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
        end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
        branches_str = request.GET.getlist("branch")
    except Exception as e:
        print(e)
    branches = []
    invoices = Invoice.objects.defer("date_created", "last_modified").values("date").annotate(sum_total_amount=Sum("total_amount")).annotate(sum_total_items=Sum("total_items")).filter(branch__pk__in=allowed_branches).order_by("date")
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            invoices = invoices.filter(date__range=(start_date, end_date))
            print(start_date, end_date)
        except Exception as e:
            print(e)
        if branches_str:
            print(branches_str)
            try:
                branches = [int(branch_str) for branch_str in branches_str if int(branch_str) in allowed_branches]
            except ValueError:
                branches = []
            if branches:
                invoices = invoices.filter(branch__pk__in=branches)

        dates = [str(row["date"].strftime("%Y-%m-%d")) for row in invoices]
        total_items = [float(row["sum_total_items"]) for row in invoices]
        total_amount = [float(row["sum_total_amount"]) for row in invoices]

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "dates": dates,
                    "total_items": total_items,
                    "total_amount": total_amount
                }
            )
    if not profile.is_manager:
        all_branches = all_branches.filter(pk__in=allowed_branches)
    return render(request, "invoice-counter.html", {"invoices": invoices, "branches": all_branches, "dates": json.dumps(dates), "total_amount": json.dumps(total_amount), "total_items": json.dumps(total_items)})
