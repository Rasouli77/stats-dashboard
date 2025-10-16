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
)
from django.db.models import Sum, Q, Min, Max, Avg, F
from .views import jalali_to_gregorian
from datetime import datetime
import math
import re
import subprocess
import jdatetime
import re
from collections import defaultdict


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
        if len(selected_grouped_campaigns) > 1:
            grouped_campaigns = (
                Campaign.objects.defer("last_modified", "date_created")
                .filter(
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash,
                    group_id__in=selected_grouped_campaigns,
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
                    invoice_amount_avg=Avg("total_amount"),
                )
                invoice_number_avg = invoice["invoice_number_avg"] or 0
                invoice_amount_avg = invoice["invoice_amount_avg"] or 0
                try:
                    conversion_rate = (invoice_number_avg / people_counting_avg) * 100
                    value_per_visitor = invoice_amount_avg / people_counting_avg
                except ZeroDivisionError as e:
                    print(e)
                    conversion_rate = 0
                    value_per_visitor = 0
                campaign["branch_names"] = ", ".join(branch_names)
                campaign["people_counting_avg"] = math.floor(people_counting_avg)
                campaign["invoice_number_avg"] = math.floor(invoice_number_avg)
                campaign["invoice_amount_avg"] = math.floor(invoice_amount_avg) // 10
                campaign["conversion_rate"] = math.floor(conversion_rate)
                campaign["value_per_visitor"] = math.floor(value_per_visitor) // 10
            return Response(list(grouped_campaigns))


class CampaignComparison(APIView):
    def get(self, request):
        selected_grouped_campaigns = request.GET.getlist("campaign")
        if len(selected_grouped_campaigns) > 1:
            selected_grouped_campaigns = [
                int(item) for item in selected_grouped_campaigns
            ]
            campaigns = (
                Campaign.objects.defer("last_modified", "date_created")
                .values("pk", "name", "start_date", "end_date", "cost", "campaign_type")
                .filter(
                    branch__merchant__url_hash=request.user.profile.merchant.url_hash,
                    pk__in=selected_grouped_campaigns,
                )
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
                    invoice_amount_avg=Avg("total_amount"),
                )
                invoice_number_avg = invoice["invoice_number_avg"] or 0
                invoice_amount_avg = invoice["invoice_amount_avg"] or 0
                try:
                    conversion_rate = (invoice_number_avg / people_counting_avg) * 100
                    value_per_visitor = invoice_amount_avg / people_counting_avg
                except ZeroDivisionError as e:
                    print(e)
                    conversion_rate = 0
                    value_per_visitor = 0
                campaign["people_counting_avg"] = math.floor(people_counting_avg)
                campaign["invoice_number_avg"] = math.floor(invoice_number_avg)
                campaign["invoice_amount_avg"] = math.floor(invoice_amount_avg) // 10
                campaign["conversion_rate"] = math.floor(conversion_rate)
                campaign["value_per_visitor"] = math.floor(value_per_visitor) // 10
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
