from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PeopleCounting, Branch, Invoice
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
        queryset = Invoice.objects.filter(branch__merchant__url_hash=request.user.profile.merchant.url_hash)
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
            branches = Branch.objects.filter(merchant__url_hash=request.user.profile.merchant.url_hash, pk__in=selected_branches)
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
                    "total_items": total_items
                }
            return Response(response)
