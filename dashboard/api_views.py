from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PeopleCounting, Branch, Invoice, PermissionToViewBranch, Campaign
from django.db.models import Sum
from django.db.models import F
from .views import jalali_to_gregorian
from datetime import datetime


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
                for invoice in queryset.filter(branch=branch):
                    amount = invoice.total_amount
                    items = invoice.total_items
                    total_amounts.append(float(amount))
                    total_items.append(float(items))
                response["invoice_data"][str(branch.pk)] = {
                    "name": branch.name,
                    "total_amounts": total_amounts,
                    "total_items": total_items,
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
                for invoice in invoice_queryset.filter(branch=branch):
                    amount = invoice.total_amount
                    items = invoice.total_items
                    total_amounts.append(float(amount))
                    total_items.append(float(items))
                response["invoice_data"][str(branch.pk)] = {
                    "name": branch.name,
                    "total_amounts": total_amounts,
                    "total_items": total_items,
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
            print(response)
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
            branch_permissions = PermissionToViewBranch.objects.defer("date_created", "date_modified").select_related("branch").filter(user=profile)
            for branch_permission in branch_permissions:
                permitted_branches_str.append(branch_permission.branch.pk)
            permitted_branches = [ int(i) for i in permitted_branches_str ]
        else:
            branches = Branch.objects.filter(merchant__url_hash=profile.merchant.url_hash)
            for branch in branches:
                permitted_branches.append(branch.pk)
        try:
            q_date = request.data.get("date")
            query_branch = request.data.get("branch")
        except Exception as e:
            print(e)
        query_date = special_jalali_to_gregorian(q_date)
        campaigns = Campaign.objects.defer("date_created", "last_modified").filter(branch__pk__in=permitted_branches, start_date__lte=query_date, end_date__gte=query_date)
        if query_branch not in ["ترافیک", "ورودی", "خروجی", "مبلغ فاکتور", "تعداد فاکتور", "درصد نرخ تبدیل (%)", "نسبت (تومان)", "نسبت (%)"]:
            campaigns = campaigns.filter(branch__name=query_branch)
        campaigns_list = []
        for campaign in campaigns:
            campaigns_list.append({
                "campaign_name": campaign.name,
                "campaign_type": campaign.campaign_type
            })
        return Response(campaigns_list)



