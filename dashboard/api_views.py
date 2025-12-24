from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    PeopleCounting,
    Branch,
    Invoice,
    PermissionToViewBranch,
    Campaign,
    HolidayDate,
    Cam,
    PeopleCountingHourly,
    WebsiteSales,
    WebsiteVisit
)
from django.db.models import Sum, Q, Min, Max, Avg, F
from .views import jalali_to_gregorian
from datetime import datetime, timedelta, time
import math
import re
import subprocess
import jdatetime
import re
from collections import defaultdict
from .ai import ai_give_answers
import json


class MultipleBranches(APIView):
    def get(self, request):
        queryset = (
            PeopleCounting.objects.filter(
                merchant__url_hash=request.user.profile.merchant.url_hash
            )
            .values("date")
            .annotate(entry_totals=Sum("entry"))
            .order_by("date")
        )
        start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
        end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
        selected_branches = request.GET.getlist("branch")
        start_date = 0
        end_date = 0
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if start_date and end_date:
            try:
                queryset = queryset.filter(date__range=(start_date, end_date))
            except Exception as e:
                print("error", e)

        dates = sorted(set(queryset.values_list("date", flat=True)))
        response = {"dates": dates, "branches": {}}
        branches = Branch.objects.filter(pk__in=selected_branches)
        for branch in branches:
            entry_totals = []
            for row in queryset.filter(branch=branch):
                count = row["entry_totals"]
                entry_totals.append(count)
            response["branches"][str(branch.pk)] = {
                "name": branch.name,
                "entry_totals": entry_totals,
            }
        return Response(response)


class MultiBranchesInvoice(APIView):
    def get(self, request):
        merchant = request.user.profile.merchant
        queryset = Invoice.objects.filter(branch__merchant__url_hash=merchant.url_hash)
        start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
        end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            try:
                queryset = queryset.filter(date__range=(start_date, end_date))
            except Exception as e:
                print(e)
        dates = sorted(set(queryset.values_list("date", flat=True)))
        response = {"dates": dates, "invoice_data": {}}
        selected_branches = request.GET.getlist("branch")
        if selected_branches:
            branches = Branch.objects.filter(
                merchant__url_hash=merchant.url_hash, pk__in=selected_branches
            )
            for branch in branches:
                total_amounts = []
                total_items = []
                total_products = []
                for invoice in queryset.filter(branch=branch):
                    amount = invoice.total_amount
                    items = invoice.total_items
                    products = invoice.total_product
                    total_amounts.append(float(amount // 10000000))
                    total_items.append(float(items))
                    total_products.append(float(products))
                response["invoice_data"][str(branch.pk)] = {
                    "name": branch.name,
                    "total_amounts": total_amounts,
                    "total_items": total_items,
                    "total_products": total_products,
                }
            return Response(response)


class Analysis(APIView):
    def get(self, request):
        merchant = request.user.profile.merchant
        people_counting_queryset = (
            PeopleCounting.objects.filter(
                merchant__url_hash=request.user.profile.merchant.url_hash
            )
            .values("date")
            .annotate(entry_totals=Sum("entry"))
            .order_by("date")
        )
        invoice_queryset = Invoice.objects.filter(
            branch__merchant__url_hash=merchant.url_hash
        )
        start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
        end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
        selected_branches = request.GET.getlist("branch")
        start_date = 0
        end_date = 0
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if start_date and end_date:
            try:
                people_counting_queryset = people_counting_queryset.filter(
                    date__range=(start_date, end_date)
                )
                invoice_queryset = invoice_queryset.filter(
                    date__range=(start_date, end_date)
                )
            except Exception as e:
                print("error", e)
        invoice_dates = sorted(set(invoice_queryset.values_list("date", flat=True)))
        people_counting_dates = sorted(
            set(people_counting_queryset.values_list("date", flat=True))
        )
        response = {
            "invoice_dates": invoice_dates,
            "invoice_data": {},
            "people_counting_dates": people_counting_dates,
            "people_counting_data": {},
        }
        if selected_branches:
            branches = Branch.objects.filter(
                merchant__url_hash=merchant.url_hash, pk__in=selected_branches
            )
            for branch in branches:
                total_amounts = []
                total_items = []
                total_products = []
                total_products_avg = []
                for invoice in invoice_queryset.filter(branch=branch):
                    amount = invoice.total_amount
                    items = invoice.total_items
                    products = invoice.total_product
                    total_amounts.append(float(amount))
                    total_items.append(float(items))
                    total_products.append(float(products))
                total_products_avg = [
                    round(float(a / b if b != 0 else 0), 1)
                    for a, b in zip(total_products, total_items)
                ]
                print(total_products)
                print(total_items)
                print(total_products_avg)
                response["invoice_data"][str(branch.pk)] = {
                    "name": branch.name,
                    "total_amounts": total_amounts,
                    "total_items": total_items,
                    "total_products_avg": total_products_avg,
                }
            for branch in branches:
                entry_totals = []
                entry_overalls = []
                for row in people_counting_queryset.filter(branch=branch):
                    count = row["entry_totals"]
                    entry_totals.append(count)
                for row in people_counting_queryset:
                    count_all = row["entry_totals"]
                    entry_overalls.append(count_all)
                response["people_counting_data"][str(branch.pk)] = {
                    "name": branch.name,
                    "entry_totals": entry_totals,
                    "entry_overalls": entry_overalls,
                }
            return Response(response)


def special_jalali_to_gregorian(jalali_str):
    import jdatetime

    english = jalali_str.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    y, m, d = map(int, english.split("/"))
    return jdatetime.date(y, m, d).togregorian()


class GetCampaignEachPoint(APIView):
    def post(self, request):
        profile = request.user.profile
        permitted_branches_str = []
        permitted_branches = []
        if not request.user.profile.is_manager:
            branch_permissions = (
                PermissionToViewBranch.objects.defer("date_created", "date_modified")
                .select_related("branch")
                .filter(user=profile)
            )
            for branch_permission in branch_permissions:
                permitted_branches_str.append(branch_permission.branch.pk)
            permitted_branches = [int(i) for i in permitted_branches_str]
        else:
            branches = Branch.objects.filter(
                merchant__url_hash=profile.merchant.url_hash
            )
            for branch in branches:
                permitted_branches.append(branch.pk)
        try:
            q_date = request.data.get("date")
            query_branch = request.data.get("branch")
            print(q_date, query_branch)
        except Exception as e:
            print(e)
        query_date = special_jalali_to_gregorian(q_date)
        campaigns = Campaign.objects.defer("date_created", "last_modified").filter(
            branch__pk__in=permitted_branches,
            start_date__lte=query_date,
            end_date__gte=query_date,
        )
        branch = Branch.objects.filter(pk__in=permitted_branches)
        branch_names = [item.name for item in branch]
        print(branch_names)
        if query_branch in branch_names:
            campaigns = campaigns.filter(branch__name=query_branch)
        print(campaigns)
        campaigns_list = []
        for campaign in campaigns:
            campaigns_list.append(
                {
                    "campaign_name": campaign.name,
                    "campaign_type": campaign.campaign_type,
                }
            )
        print(campaigns_list)
        unique_list = []
        for d in campaigns_list:
            if d not in unique_list:
                unique_list.append(d)
        campaigns_list = unique_list
        print(campaigns_list)
        return Response(campaigns_list)


class GroupedCampaigns(APIView):
    def get(self, request):
        start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
        end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
        start_date = None
        end_date = None
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except:
            pass
        if start_date and end_date:
            campaigns = (
                Campaign.objects.filter(
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash
                )
                .filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date))
                .values("group_id")
                .annotate(
                    campaign_name=Min("name"),
                    campaign_start_date=Min("start_date"),
                    campaign_end_date=Max("end_date"),
                    campaign_cost=Sum("cost"),
                    campaign_type=Min("campaign_type"),
                    campaign_last_modified=Max("last_modified"),
                    campaign_group_id=Min("group_id"),
                )
                .order_by("-campaign_last_modified")
            )
        else:
            campaigns = (
                Campaign.objects.filter(
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash
                )
                .values("group_id")
                .annotate(
                    campaign_name=Min("name"),
                    campaign_start_date=Min("start_date"),
                    campaign_end_date=Max("end_date"),
                    campaign_cost=Sum("cost"),
                    campaign_type=Min("campaign_type"),
                    campaign_last_modified=Max("last_modified"),
                    campaign_group_id=Min("group_id"),
                )
                .order_by("-campaign_last_modified")
            )

        for campaign in campaigns:
            branch_names = (
                Campaign.objects.filter(group_id=campaign["campaign_group_id"])
                .values_list("branch__name", flat=True)
                .distinct()
            )
            campaign["branch_names"] = ", ".join(branch_names)

        campaign_list = []
        dictionary = {}
        for campaign in campaigns:
            dictionary = {
                "campaign_name": campaign["campaign_name"],
                "campaign_start_date": campaign["campaign_start_date"],
                "campaign_end_date": campaign["campaign_end_date"],
                "branches": campaign["branch_names"],
                "campaign_cost": campaign["campaign_cost"],
                "campaign_type": campaign["campaign_type"],
            }
            campaign_list.append(dictionary)
        return Response(campaign_list)


class GroupedCampaignComparison(APIView):
    def get(self, request):
        selected_grouped_campaigns = request.GET.getlist("grouped-campaign")
        print(selected_grouped_campaigns)
        if len(selected_grouped_campaigns) > 1:
            # each item looks like this: "تست""
            grouped_campaigns = (
                Campaign.objects.defer("last_modified", "date_created")
                .filter(
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash,
                    name__in=selected_grouped_campaigns,
                )
                .values("group_id")
                .annotate(
                    campaign_name=Min("name"),
                    campaign_start_date=Min("start_date"),
                    campaign_end_date=Max("end_date"),
                    campaign_cost=Sum("cost"),
                    campaign_type=Min("campaign_type"),
                    campaign_last_modified=Max("last_modified"),
                    campaign_group_id=Min("group_id"),
                )
                .order_by("-campaign_last_modified")
            )
            for campaign in grouped_campaigns:
                branch = (
                    Campaign.objects.filter(group_id=campaign["campaign_group_id"])
                    .values_list("branch__pk", "branch__name")
                    .distinct()
                )
                branch_pks, branch_names = zip(*branch) if branch else ([], [])
                branch_pks = [int(item) for item in branch_pks]
                people_counting_avg = PeopleCounting.objects.filter(
                    merchant__url_hash=request.user.profile.merchant.url_hash,
                    date__range=(
                        campaign["campaign_start_date"],
                        campaign["campaign_end_date"],
                    ),
                    branch__pk__in=list(branch_pks),
                ).aggregate(entry_avg=Avg("entry"))
                people_counting_avg = people_counting_avg["entry_avg"] or 0
                invoice = Invoice.objects.filter(
                    branch__pk__in=list(branch_pks),
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash,
                    date__range=(
                        campaign["campaign_start_date"],
                        campaign["campaign_end_date"],
                    ),
                ).aggregate(
                    invoice_number_avg=Avg("total_items"),
                    product=Avg("total_product"),
                    invoice_amount_avg=Avg("total_amount"),
                )
                invoice_number_avg = invoice["invoice_number_avg"] or 0
                product = invoice["product"] or 0
                invoice_amount_avg = invoice["invoice_amount_avg"] or 0
                try:
                    conversion_rate = (invoice_number_avg / people_counting_avg) * 100
                    value_per_visitor = invoice_amount_avg / people_counting_avg
                    cart = product / invoice_number_avg 
                except ZeroDivisionError as e:
                    print(e)
                    conversion_rate = 0
                    value_per_visitor = 0
                    cart = 0
                campaign["branch_names"] = ", ".join(branch_names)
                campaign["people_counting_avg"] = math.floor(people_counting_avg)
                campaign["invoice_number_avg"] = math.floor(invoice_number_avg)
                campaign["product"] = math.floor(product)
                campaign["invoice_amount_avg"] = math.floor(invoice_amount_avg) // 10
                campaign["conversion_rate"] = math.floor(conversion_rate)
                campaign["cart"] = math.floor(cart)
                campaign["value_per_visitor"] = math.floor(value_per_visitor) // 10
            print(list(grouped_campaigns))
            return Response(list(grouped_campaigns))


class CampaignComparison(APIView):
    def get(self, request):
        selected_single_campaigns = request.GET.getlist("campaign")
        print(selected_single_campaigns)
        q_object = Q()
        if len(selected_single_campaigns) > 1:
            # each item looks like this: "تست - اقدسیه"
            for item in selected_single_campaigns:
                name, branch_name = item.split("-", 1)
                name = name.strip()
                branch_name = branch_name.strip()
                q_object |= Q(name=name, branch__name=branch_name)
            campaigns = (
                Campaign.objects.defer("last_modified", "date_created")
                .values("pk", "name", "start_date", "end_date", "cost", "campaign_type")
                .filter(
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash,
                )
                .filter(q_object)
                .annotate(branch_name=F("branch__name"), branch_pk=F("branch__pk"))
            )
            for campaign in campaigns:
                people_counting_avg = PeopleCounting.objects.filter(
                    merchant__url_hash=request.user.profile.merchant.url_hash,
                    date__range=(campaign["start_date"], campaign["end_date"]),
                    branch__pk=campaign["branch_pk"],
                ).aggregate(entry_avg=Avg("entry"))
                people_counting_avg = people_counting_avg["entry_avg"] or 0
                invoice = Invoice.objects.filter(
                    branch__pk=campaign["branch_pk"],
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash,
                    date__range=(campaign["start_date"], campaign["end_date"]),
                ).aggregate(
                    invoice_number_avg=Avg("total_items"),
                    product=Avg("total_product"),
                    invoice_amount_avg=Avg("total_amount"),
                )
                invoice_number_avg = invoice["invoice_number_avg"] or 0
                product = invoice["product"] or 0
                invoice_amount_avg = invoice["invoice_amount_avg"] or 0
                try:
                    conversion_rate = (invoice_number_avg / people_counting_avg) * 100
                    value_per_visitor = invoice_amount_avg / people_counting_avg
                    cart = product / invoice_number_avg
                except ZeroDivisionError as e:
                    print(e)
                    conversion_rate = 0
                    value_per_visitor = 0
                    cart = 0
                campaign["people_counting_avg"] = math.floor(people_counting_avg)
                campaign["invoice_number_avg"] = math.floor(invoice_number_avg)
                campaign["product"] = math.floor(product)
                campaign["invoice_amount_avg"] = math.floor(invoice_amount_avg) // 10
                campaign["conversion_rate"] = math.floor(conversion_rate)
                campaign["value_per_visitor"] = math.floor(value_per_visitor) // 10
                campaign["cart"] = math.floor(cart)
            print(list(campaigns))
            return Response(list(campaigns))


def to_persian_digits(number_str: str) -> str:
    persian_digits = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }
    return "".join(persian_digits.get(ch, ch) for ch in number_str)


def to_english_digits(number_str: str) -> str:
    english_digits = {
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
    }
    return "".join(english_digits.get(ch, ch) for ch in number_str)


class HolidaySpotter(APIView):
    def get(self, request):
        try:
            start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
            end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
            if start_date_str and end_date_str:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
                holidays = HolidayDate.objects.filter(
                    gregorian_date__range=(start_date, end_date)
                )
                complete_holiday_dates = []
                dictionary = {}
                descriptions_for_each_holiday = []
                for holiday in holidays:
                    dictionary = {}
                    dictionary["date"] = to_persian_digits(holiday.date)
                    descriptions_for_each_holiday = []
                    descriptions = holiday.holidaydsc.all()
                    if descriptions:
                        for x in descriptions:
                            descriptions_for_each_holiday.append(x.description)
                        dictionary["descriptions"] = descriptions_for_each_holiday
                    complete_holiday_dates.append(dictionary)
                return Response(complete_holiday_dates)
            else:
                return Response({"error": f"{e}"})
        except Exception as e:
            print(e)
            return Response({"error": f"{e}"})


def ping_ip(ip, timeout=15):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 2,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"Timeout: Ping to {ip} took too long.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def get_ping(ip, timeout=15):
    try:
        # Run ping command and capture output
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout + 2,
        )

        if result.returncode == 0:
            # Example ping output line on Linux:
            match = re.search(r"time=([\d.]+)\s*ms", result.stdout)
            if match:
                return int(float(match.group(1)))  # return RTT in ms
            else:
                return None
        else:
            return None

    except subprocess.TimeoutExpired:
        print(f"Timeout: Ping to {ip} took too long.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


class CamStatus(APIView):
    def post(self, request):
        try:
            raw_cam_id = str(request.data.get("id"))
            cam_id = int(to_english_digits(raw_cam_id))
            cam = Cam.objects.get(pk=cam_id)
            if ping_ip(cam.ip):
                cam.status = True
                cam.save()
                ping = get_ping(cam.ip)
                return Response({"cam_id": cam.pk, "status": cam.status, "ping": ping})
            else:
                cam.status = False
                cam.save()
                return Response({"cam_id": cam.pk, "status": cam.status})
        except Exception as e:
            return Response({"error": f"{e}"})


PERSIAN_TO_ENGLISH_MAPPING = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")


ENGLISH_TO_PERSIAN_MAPPING = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def ascii_to_persian(s: str) -> str:
    s = s.strip()
    return s.translate(ENGLISH_TO_PERSIAN_MAPPING)


def persian_to_ascii(s: str) -> str:
    s = s.strip()
    return s.translate(PERSIAN_TO_ENGLISH_MAPPING)


def persian_date_to_jdate(s: str):
    s = persian_to_ascii(s)
    parts = re.split(r"[\/\-\.]", s)
    y, m, d = map(int, parts)
    return jdatetime.date(y, m, d)


def persian_date_eng_digit_to_jdate(s: str):
    parts = re.split(r"[\/\-\.]", s)
    y, m, d = map(int, parts)
    return jdatetime.date(y, m, d)


def divide_monthly(dates, values):
    monthly_data = defaultdict(int)
    for d, v in zip(dates, values):
        date = persian_date_to_jdate(d)
        year = date.year
        month = date.month
        if len(str(month)) == 1:
            key = f"{year}/0{month}"
        else:
            key = f"{year}/{month}"
        monthly_data[key] += v
    sorted_monthly_data = sorted(
        monthly_data.items(), key=lambda item: int(re.sub("/", "", item[0]))
    )
    monthly_data = dict(sorted_monthly_data)
    monthly_data_output = {}
    for k, v in monthly_data.items():
        monthly_data_output[ascii_to_persian(k)] = v
    months = list(monthly_data_output.keys())
    values = list(monthly_data_output.values())
    return months, values


def divide_monthly_avg(dates, values):
    monthly_data = defaultdict(int)
    counter = 0
    counter_list = []
    for d, v in zip(dates, values):
        date = persian_date_to_jdate(d)
        year = date.year
        month = date.month
        if len(str(month)) == 1:
            key = f"{year}/0{month}"
        else:
            key = f"{year}/{month}"
        if key in monthly_data.keys():
            counter += 1
        else:
            if counter != 0:
                counter_list.append(counter + 1)
            counter = 0
        monthly_data[key] += v
    sorted_monthly_data = sorted(
        monthly_data.items(), key=lambda item: int(re.sub("/", "", item[0]))
    )
    monthly_data = dict(sorted_monthly_data)
    monthly_data_output = {}
    for k, v in monthly_data.items():
        monthly_data_output[ascii_to_persian(k)] = v
    months = list(monthly_data_output.keys())
    values = list(monthly_data_output.values())
    avg_values = [math.floor(a/b) if b != 0 else 0 for a, b in zip(values, counter_list)]
    return months, avg_values


def divide_weekly(dates, values):
    weekly_data = defaultdict(int)
    for d, v in zip(dates, values):
        date = persian_date_to_jdate(d)
        year = date.year
        week = date.isocalendar()[1]
        key = f"هفته {week}"
        weekly_data[key] += v
    sorted_weekly_data = sorted(
        weekly_data.items(), key=lambda item: int(re.findall(r"\d+", item[0])[0])
    )
    weekly_data = dict(sorted_weekly_data)
    weekly_data_output = {}
    for k, v in weekly_data.items():
        weekly_data_output[f"هفته {ascii_to_persian(re.findall(r'\d+', k)[0])}"] = v
    weeks = list(weekly_data_output.keys())
    values = list(weekly_data_output.values())
    return weeks, values


def divide_weekly_avg(dates, values):
    weekly_data = defaultdict(int)
    counter = 0
    counter_list = []
    for d, v in zip(dates, values):
        date = persian_date_to_jdate(d)
        year = date.year
        week = date.isocalendar()[1]
        key = f"هفته {week}"
        if key in weekly_data.keys():
            counter += 1
        else:
            if counter != 0:
                counter_list.append(counter + 1)
            counter = 0
        weekly_data[key] += v
    sorted_weekly_data = sorted(
        weekly_data.items(), key=lambda item: int(re.findall(r"\d+", item[0])[0])
    )
    weekly_data = dict(sorted_weekly_data)
    weekly_data_output = {}
    for k, v in weekly_data.items():
        weekly_data_output[f"هفته {ascii_to_persian(re.findall(r'\d+', k)[0])}"] = v
    weeks = list(weekly_data_output.keys())
    values = list(weekly_data_output.values())
    avg_values = [math.floor(a/b) if b != 0 else 0 for a, b in zip(values, counter_list)]
    return weeks, avg_values


class NormalWeeklyDisplay(APIView):
    def post(self, request):
        try:
            x = request.data.get("x")
            y = request.data.get("y")
            weeks, values = divide_weekly(x, y)
            return Response({"weeks": weeks, "values": values})
        except Exception as e:
            return Response({"error": f"{e}"})


class abNormalWeeklyDisplay(APIView):
    def post(self, request):
        try:
            x = request.data.get("x")
            y = request.data.get("y")
            values = []
            x_dict = {}
            weeks = []
            for dictionary in y:
                x_dict = {}
                x_dict["name"] = dictionary["name"]
                x_dict["data"] = divide_weekly(x, dictionary["data"])[1]
                if not weeks:
                    weeks = divide_weekly(x, dictionary["data"])[0]
                values.append(x_dict)
            print({"weeks": weeks, "values": values})
            return Response({"weeks": weeks, "values": values})
        except Exception as e:
            return Response({"error": f"{e}"})


class NormalMonthlyDisplay(APIView):
    """
    This is related to sending data to normal charts.
    Whenever the monthly display button is pushed on the front-end, it sends a request to this API.
    It then send a dictionary which contains 2 lists: months and values.
    """

    def post(self, request):
        """
        A request of type post must be sent to this API otherwise, it sends an error.
        It must get 2 lists: 1. dates 2. values in order to work properly.
        The divide_monthly function is used here in a pretty straightforward way.
        """
        try:
            x = request.data.get("x")
            y = request.data.get("y")
            months, values = divide_monthly(x, y)
            return Response({"months": months, "values": values})
        except Exception as e:
            return Response({"error": f"{e}"})


class abNormalMonthlyDisplay(APIView):
    """
    This class-based view differs from the normal monthly display as it deals with separate-branch charts.
    This is related to sending data to separate-branch charts.
    Whenever the monthly display button is pushed on the front-end, it sends a request to this API.
    It then send a dictionary which contains 2 lists: months and values.
    """

    def post(self, request):
        """
        A request of type post must be sent to this API otherwise, it sends an error.
        It must get 2 lists: 1. dates 2. values in order to work properly.
        The divide_monthly function is used here but in a different way.
        """
        try:
            x = request.data.get("x")
            y = request.data.get("y")
            values = []
            x_dict = {}
            months = []
            for dictionary in y:
                x_dict = {}
                x_dict["name"] = dictionary["name"]
                x_dict["data"] = divide_monthly(x, dictionary["data"])[1]
                if not months:
                    months = divide_monthly(x, dictionary["data"])[0]
                values.append(x_dict)
            return Response({"months": months, "values": values})
        except Exception as e:
            return Response({"error": f"{e}"})


class AI(APIView):
    def post(self, request):
        """
        We have 4 variables that get posted to this API:
        1. Which area to focus on: (traffic, sales, conversion rate)
        2. What is the type of the said chart: a stands for aggregated: true or false
        3. No matter what they want, we always send all data associated with the specified time period
        4. As well as holidays
        5. And campaigns
        (only the emphasis shifts based on the variable e)
        The data we send within the specified time line for both types (the t variable):
        1. invoice count 
        2. invoice amount
        3. invoice product count
        4. traffic
        """
        # Emphasis
        e = request.data.get("e")
        # Type: a stands for aggregated: true or false
        a = request.data.get("a")
        # Start Date
        raw_start_date = request.data.get("aiStartDate")
        # End Date
        raw_end_date = request.data.get("aiEndDate")
        # Branch ID
        branch_ids = [int(x) for x in request.data.get("aiBranchIds")]

        # Dates
        start_jdate = persian_date_eng_digit_to_jdate(raw_start_date)
        end_jdate = persian_date_eng_digit_to_jdate(raw_end_date)
        start_date = start_jdate.togregorian()
        end_date = end_jdate.togregorian()

        # Difference
        difference = (end_date - start_date).days
        print(difference)
        if difference < 10:
            return Response({"ai":"برای تحلیل هوش مصنوعی نیاز است که بازه ای بیشتر از 10 روز انتخاب شود."})

        # Database
        # url hash
        url_hash = request.user.profile.merchant.url_hash
        # all branches count for the account
        branch_count = Branch.objects.filter(merchant__url_hash=url_hash).count()

        # Campaigns
        campaigns = (
            Campaign.objects.filter(
                branch__merchant__url_hash=request.user.profile.merchant.url_hash
            )
            .filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date))
            .values("group_id")
            .annotate(
                campaign_name=Min("name"),
                campaign_start_date=Min("start_date"),
                campaign_end_date=Max("end_date"),
                campaign_cost=Sum("cost"),
                campaign_type=Min("campaign_type"),
                campaign_last_modified=Max("last_modified"),
                campaign_group_id=Min("group_id"),
            )
            .order_by("-campaign_last_modified")
        )
        for campaign in campaigns:
            branch_names = (
                Campaign.objects.filter(group_id=campaign["campaign_group_id"])
                .values_list("branch__name", flat=True)
                .distinct()
            )
            campaign["branch_names"] = ", ".join(branch_names)
        campaign_list = []
        dictionary = {}
        for campaign in campaigns:
            dictionary = {
                "campaign_name": campaign["campaign_name"],
                "campaign_start_date": campaign["campaign_start_date"],
                "campaign_end_date": campaign["campaign_end_date"],
                "branches": campaign["branch_names"],
                "campaign_cost": campaign["campaign_cost"],
                "campaign_type": campaign["campaign_type"],
            }
            campaign_list.append(dictionary)
        for i in campaign_list:
            i["campaign_start_date"] = i["campaign_start_date"].isoformat()
            i["campaign_end_date"] = i["campaign_end_date"].isoformat()
        # Holidays
        holidays = HolidayDate.objects.filter(
            gregorian_date__range=(start_date, end_date)
        )
        complete_holiday_dates = []
        dictionary = {}
        descriptions_for_each_holiday = []
        for holiday in holidays:
            dictionary = {}
            dictionary["date"] = to_persian_digits(holiday.date)
            descriptions_for_each_holiday = []
            descriptions = holiday.holidaydsc.all()
            if descriptions:
                for x in descriptions:
                    descriptions_for_each_holiday.append(x.description)
                dictionary["descriptions"] = descriptions_for_each_holiday
            complete_holiday_dates.append(dictionary)

        # aggregated
        if a:
            try:
                traffic = (
                PeopleCounting.objects.defer("date_created", "last_modified", "cam")
                .filter(merchant__url_hash=url_hash, date__range=(start_date, end_date))
                .values("date")
                .annotate(total_entry=Sum("entry"))
                .order_by("date")
                )

                invoices = (
                    Invoice.objects.defer("date_created", "last_modified")
                    .select_related("branch", "branch__merchant")
                    .filter(branch__merchant__url_hash=url_hash, date__range=(start_date, end_date))
                    .values("date")
                    .annotate(
                        sum_total_amount=Sum("total_amount"),
                        sum_total_items=Sum("total_items"),
                        sum_total_products=Sum("total_product"),
                    )
                    .order_by("date")
                )

                # if some branches are selected
                if len(branch_ids) != branch_count:
                    traffic = traffic.filter(branch__pk__in=branch_ids)
                    invoices = invoices.filter(branch__pk__in=branch_ids)

                # Dates
                dates = [str(row["date"].strftime("%Y-%m-%d")) for row in invoices]

                # Data for AI
                total_entries = [float(row["total_entry"]) for row in traffic]
                invoice_items = [float(row["sum_total_items"]) for row in invoices]
                invoice_amounts = [float(row["sum_total_amount"] // 10000000) for row in invoices]
                invoice_products = [float(row["sum_total_products"]) for row in invoices]

                # AI Integration
                print("total_entries", total_entries)
                print("invoice_items", invoice_items)
                print("invoice_products", invoice_products)
                print("invoice_amounts", invoice_amounts)
                print("complete_holiday_dates", complete_holiday_dates)
                print("campaign_list", campaign_list)
                print("dates", dates)

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional data analyst who responds only in Persian."
                            "Do not talk about specific dates. Only focus on Averages over the course of periods of time. Never Focus on specific dates."
                            "Turn all dates to jalali. Do not mention gregorian dates."
                            "Traffic entering the branches is represented by total_entries."
                            "All dates are ordered from left to right, and each value in every list corresponds to the same day in the dates list. "
                            "The data also includes campaigns and holidays with their respective dates or date ranges."
                            "As a data expert, analyze the data carefully: identify trends, patterns, and anomalies;"
                            "explain averages, percentage changes, and growth rates when relevant;"
                            "and always consider the effects of campaigns and holidays."
                            "Mention each campaign specifically and judge them"
                            "Finish your response with exactly two practical business suggestions."
                            "Do not use HTML in your response — use plain text styling instead."
                            "At the end, make sure your final Persian response contains no English or Chinese words or characters; remove them if necessary."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Analyze this data:\n"
                            f"total_entries (traffic) = {json.dumps(total_entries, ensure_ascii=False)}\n"
                            f"invoice_items (number of invoices) = {json.dumps(invoice_items, ensure_ascii=False)}\n"
                            f"invoice_products (number of sold products) = {json.dumps(invoice_products, ensure_ascii=False)}\n"
                            f"invoice_amounts (sales amounts in million tomans) = {json.dumps(invoice_amounts, ensure_ascii=False)}\n"
                            f"complete_holiday_dates = {json.dumps(complete_holiday_dates, ensure_ascii=False)}\n"
                            f"campaign_list = {json.dumps(campaign_list, ensure_ascii=False)}\n"
                            f"dates = {json.dumps(dates, ensure_ascii=False)}\n"
                            f"The focus of your analysis must be on: {e}. 30% must be on other data above."
                            "Do not talk about specific dates. Only focus on Averages over the course of periods of time. Never Focus on specific dates."
                        )
                    }
                ]
                ai_response = ai_give_answers(messages, 0.5)
                return Response({"ai": ai_response})
            except Exception as e:
                print(e)
                return Response({"error": f"{e}"})
        else:
            try:
                traffic = (
                    PeopleCounting.objects.filter(
                        merchant__url_hash=url_hash, date__range=(start_date, end_date)
                    )
                    .values("date")
                    .annotate(entry_totals=Sum("entry"))
                    .order_by("date")
                )
                invoices = Invoice.objects.filter(branch__merchant__url_hash=url_hash, date__range=(start_date, end_date))
                dates = sorted(set(traffic.values_list("date", flat=True)))
                dates = [date.isoformat() for date in dates]
                traffic_response = {"dates": dates, "branches": {}}
                invoice_response = {"dates": dates, "invoice_data": {}}

                branches = Branch.objects.filter(merchant__url_hash=url_hash, pk__in=branch_ids)
                for branch in branches:
                    entry_totals = []
                    total_amounts = []
                    total_items = []
                    total_products = []
                    # traffic loop
                    for row in traffic.filter(branch=branch):
                        count = row["entry_totals"]
                        entry_totals.append(count)
                    # Data for AI
                    traffic_response["branches"][str(branch.pk)] = {
                        "name": branch.name,
                        "entry_totals": entry_totals,
                    }
                    # invoice loop
                    for invoice in invoices.filter(branch=branch):
                        amount = invoice.total_amount
                        items = invoice.total_items
                        products = invoice.total_product
                        total_amounts.append(float(amount // 10000000))
                        total_items.append(float(items))
                        total_products.append(float(products))
                    # Data for AI
                    invoice_response["invoice_data"][str(branch.pk)] = {
                        "name": branch.name,
                        "total_amounts": total_amounts,
                        "total_items": total_items,
                        "total_products": total_products,
                    }
                # AI Integration
                print("traffic_response", traffic_response)
                print("invoice_response", invoice_response)
                print("complete_holiday_dates", complete_holiday_dates)
                print("campaign_list", campaign_list)
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional data analyst who responds only in Persian."
                            "Do not talk about specific dates. Only focus on Averages over the course of periods of time. Never Focus on specific dates."
                            "Turn all dates to jalali. Do not mention gregorian dates."
                            "Traffic entering the branches is represented by total_entries."
                            "All dates are ordered from left to right, and each value in every list corresponds to the same day in the dates list."
                            "The data also includes campaigns and holidays with their respective dates or date ranges."
                            "As a data expert, analyze the data carefully: identify trends, patterns, and anomalies"
                            "explain averages, percentage changes, and growth rates when relevant;"
                            "and always consider the effects of campaigns and holidays."
                            "Mention each campaign specifically and judge them"
                            "Finish your response with exactly two practical business suggestions."
                            "Do not use HTML in your response — use plain text styling instead."
                            "At the end, make sure your final Persian response contains no English or Chinese words or characters; remove them if necessary."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Analyze this data:\n"
                            f"traffic_response (traffic) separated by branch = {json.dumps(traffic_response, ensure_ascii=False)}\n"
                            f"invoice_response (total_amounts: sales amounts in million tomans) (total_items: number of invoices) (total_products: number of sold products) = {json.dumps(invoice_response, ensure_ascii=False)}\n"
                            f"complete_holiday_dates = {json.dumps(complete_holiday_dates, ensure_ascii=False)}\n"
                            f"campaign_list = {json.dumps(campaign_list, ensure_ascii=False)}\n"
                            f"dates = {json.dumps(dates, ensure_ascii=False)}\n"
                            f"70% of your focus must be on: {e}. 30% must be on other data above. "
                            "Do not talk about specific dates. Only focus on Averages over the course of periods of time. Never Focus on specific dates."
                        )
                    }
                ]
                ai_response = ai_give_answers(messages, 0.5)
                return Response({"ai": ai_response})
            except Exception as e:
                return Response({"error": f"{e}"})


class AIWebsite(APIView):
    def post(self, request):
        """
        We have 4 variables that get posted to this API:
        1. Which area to focus on: (traffic, sales, conversion rate)
        2. What is the type of the said chart: a stands for aggregated: true or false
        3. No matter what they want, we always send all data associated with the specified time period
        4. As well as holidays
        5. And campaigns
        (only the emphasis shifts based on the variable e)
        The data we send within the specified time line for both types (the t variable):
        1. invoice count 
        2. invoice amount
        3. invoice product count
        4. traffic
        """
        # Emphasis
        e = request.data.get("e")
        # Type: a stands for aggregated: true or false
        a = request.data.get("a")
        # Start Date
        raw_start_date = request.data.get("aiStartDate")
        # End Date
        raw_end_date = request.data.get("aiEndDate")

        # Dates
        start_jdate = persian_date_eng_digit_to_jdate(raw_start_date)
        end_jdate = persian_date_eng_digit_to_jdate(raw_end_date)
        start_date = start_jdate.togregorian()
        end_date = end_jdate.togregorian()

        # Difference
        difference = (end_date - start_date).days
        print(difference)
        if difference < 10:
            return Response({"ai":"برای تحلیل هوش مصنوعی نیاز است که بازه ای بیشتر از 10 روز انتخاب شود."})

        # Database
        # url hash
        url_hash = request.user.profile.merchant.url_hash

        # Campaigns
        campaigns = (
            Campaign.objects.filter(
                branch__merchant__url_hash=request.user.profile.merchant.url_hash
            )
            .filter(Q(start_date__lte=end_date) & Q(end_date__gte=start_date))
            .values("group_id")
            .annotate(
                campaign_name=Min("name"),
                campaign_start_date=Min("start_date"),
                campaign_end_date=Max("end_date"),
                campaign_cost=Sum("cost"),
                campaign_type=Min("campaign_type"),
                campaign_last_modified=Max("last_modified"),
                campaign_group_id=Min("group_id"),
            )
            .order_by("-campaign_last_modified")
        )
        for campaign in campaigns:
            branch_names = (
                Campaign.objects.filter(group_id=campaign["campaign_group_id"])
                .values_list("branch__name", flat=True)
                .distinct()
            )
            campaign["branch_names"] = ", ".join(branch_names)
        campaign_list = []
        dictionary = {}
        for campaign in campaigns:
            dictionary = {
                "campaign_name": campaign["campaign_name"],
                "campaign_start_date": campaign["campaign_start_date"],
                "campaign_end_date": campaign["campaign_end_date"],
                "branches": campaign["branch_names"],
                "campaign_cost": campaign["campaign_cost"],
                "campaign_type": campaign["campaign_type"],
            }
            campaign_list.append(dictionary)
        for i in campaign_list:
            i["campaign_start_date"] = i["campaign_start_date"].isoformat()
            i["campaign_end_date"] = i["campaign_end_date"].isoformat()
        # Holidays
        holidays = HolidayDate.objects.filter(
            gregorian_date__range=(start_date, end_date)
        )
        complete_holiday_dates = []
        dictionary = {}
        descriptions_for_each_holiday = []
        for holiday in holidays:
            dictionary = {}
            dictionary["date"] = to_persian_digits(holiday.date)
            descriptions_for_each_holiday = []
            descriptions = holiday.holidaydsc.all()
            if descriptions:
                for x in descriptions:
                    descriptions_for_each_holiday.append(x.description)
                dictionary["descriptions"] = descriptions_for_each_holiday
            complete_holiday_dates.append(dictionary)

        # aggregated
        if a:
            try:
                queryset = (
                    WebsiteVisit.objects.defer("date_created", "last_modified")
                    .filter(merchant__url_hash=url_hash, date__range=(start_date, end_date))
                    .values("date")
                    .annotate(total_entry=Sum("unique_visitors"), visits=Sum("visits"), bounce_rate=Sum('bounce_rate'), actions_count=Sum('actions_count'), sum_time_spent=Sum('sum_time_spent'), avg_time_spent=Sum('avg_time_spent'), actions_per_visit=Sum('actions_per_visit'))
                    .order_by("date")
                )
                queryset_sales = (
                    WebsiteSales.objects.defer("date_created", "last_modified")
                    .filter(merchant__url_hash=url_hash, date__range=(start_date, end_date))
                    .values("date")
                    .annotate(invoice_amount=Sum("invoice_amount"), invoice_count=Sum("invoice_count"), product_count=Sum("product_count"))
                    .order_by("date")
                )

                # Dates
                dates = [str(row["date"].strftime("%Y-%m-%d")) for row in queryset]

                # Data for AI
                entry_totals = [float(row["total_entry"]) for row in queryset]
                visits = [float(row['visits']) for row in queryset]
                bounce_rate = [float(row['bounce_rate']) for row in queryset]
                avg_time_spent = [float(row['avg_time_spent']) for row in queryset]
                invoice_amount = [float(row['invoice_amount']) / 10 for row in queryset_sales]
                invoice_count = [float(row['invoice_count']) for row in queryset_sales]
                product_count = [float(row['product_count']) for row in queryset_sales]

                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional data analyst who responds only in Persian."
                            "Do not talk about specific dates. Only focus on Averages over the course of periods of time. Never Focus on specific dates."
                            "Turn all dates to jalali. Do not mention gregorian dates."
                            "Traffic entering the branches is represented by total_entries."
                            "All dates are ordered from left to right, and each value in every list corresponds to the same day in the dates list. "
                            "The data also includes campaigns and holidays with their respective dates or date ranges."
                            "As a data expert, analyze the data carefully: identify trends, patterns, and anomalies;"
                            "explain averages, percentage changes, and growth rates when relevant;"
                            "and always consider the effects of campaigns and holidays."
                            "Mention each campaign specifically and judge them"
                            "Finish your response with exactly two practical business suggestions."
                            "Do not use HTML in your response — use plain text styling instead."
                            "At the end, make sure your final Persian response contains no English or Chinese words or characters; remove them if necessary."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Analyze this data:\n"
                            f"total entries (traffic) on our website = {json.dumps(entry_totals, ensure_ascii=False)}\n"
                            f"vists = {json.dumps(visits, ensure_ascii=False)}\n"
                            f"bounce_rate = {json.dumps(bounce_rate, ensure_ascii=False)}\n"
                            f"avg_time_spent (average time each user spent on website in seconds)= {json.dumps(avg_time_spent, ensure_ascii=False)}\n"
                            f"invoice items (number of invoices) = {json.dumps(invoice_count, ensure_ascii=False)}\n"
                            f"invoice products (number of sold products) = {json.dumps(product_count, ensure_ascii=False)}\n"
                            f"invoice amounts (sales amounts in tomans) = {json.dumps(invoice_amount, ensure_ascii=False)}\n"
                            f"complete_holiday_dates = {json.dumps(complete_holiday_dates, ensure_ascii=False)}\n"
                            f"campaign_list = {json.dumps(campaign_list, ensure_ascii=False)}\n"
                            f"dates = {json.dumps(dates, ensure_ascii=False)}\n"
                            f"The focus of your analysis must be on: {e}. 30% must be on other data above."
                            "Do not talk about specific dates. Only focus on Averages over the course of periods of time. Never Focus on specific dates."
                        )
                    }
                ]
                ai_response = ai_give_answers(messages, 0.5)
                return Response({"ai": ai_response})
            except Exception as e:
                print(e)
                return Response({"error": f"{e}"})


class MultipleBranchesHourly(APIView):
    def get(self, request):
        queryset = []
        start_date_str = str(jalali_to_gregorian(request.GET.get("start-date")))
        end_date_str = str(jalali_to_gregorian(request.GET.get("end-date")))
        selected_branches = request.GET.getlist("branch")
        start_date = 0
        end_date = 0
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        try:
            start_hour = int(request.GET.get("start-hour"))
            end_hour = int(request.GET.get("end-hour"))
        except Exception as e:
            print(e)
            start_hour, end_hour = 0, 0
    
        if start_hour > end_hour:
            start_hour, end_hour = 0, 0

        if start_date and end_date:
            try:
                queryset = (
                    PeopleCountingHourly.objects.filter(
                        merchant__url_hash=request.user.profile.merchant.url_hash, date__range=(start_date, end_date)
                    )
                    .values("hour")
                    .annotate(entry_totals=Sum("entry"))
                    .order_by("date", "hour")
                )
            except Exception as e:
                print("error", e)
            if start_hour and end_hour:
                if start_hour <= end_hour:
                    start_hour = time(start_hour, 0)
                    end_hour = time(end_hour, 0)
                    queryset = (
                        PeopleCountingHourly.objects.filter(
                            merchant__url_hash=request.user.profile.merchant.url_hash, date__range=(start_date, end_date), hour__gte=start_hour, hour__lte=end_hour
                        )
                        .values("hour")
                        .annotate(entry_totals=Sum("entry"))
                        .order_by("date", "hour")
                    )
                

            hours = sorted(set(queryset.values_list("hour", flat=True)))
            response = {"hours": hours, "branches": {}}
            hours_len = len(response["hours"])
            branches = Branch.objects.filter(pk__in=selected_branches)
            for branch in branches:
                entry_totals = []
                for row in queryset.filter(branch=branch):
                    count = row["entry_totals"]
                    entry_totals.append(count)
                list_chunks = [entry_totals[i:i+hours_len] for i in range(0, len(entry_totals), hours_len)]
                base_list = [0]*hours_len
                for item in list_chunks:
                    base_list = [x + y for x, y in zip(base_list, item)]
                entry_totals = base_list
                response["branches"][str(branch.pk)] = {
                    "name": branch.name,
                    "entry_totals": entry_totals,
                }
            print(response)
            return Response(response)
