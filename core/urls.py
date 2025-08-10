"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from accounts.views import custom_login
from dashboard.views import (
    people_counter,
    users_list,
    generate_user,
    user_permissions,
    home,
    test,
    profile,
    branch_permissions,
    campaign,
    create_campaign,
    edit_campaign,
    delete_campaign,
    upload_excel_file_invoice,
    invoices,
    invoice_detail,
    invoice_delete,
    excel_template_generator,
    invoice_counter,
    analysis,
    campaign_detail
)
from dashboard.api_views import MultipleBranches, MultiBranchesInvoice, Analysis, GetCampaignEachPoint
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.site.site_header = "پنل مدیریت فروشگاه"
admin.site.site_title = "وب‌پوش | مدیریت"
admin.site.index_title = "خوش آمدید به بخش مدیریت"


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "dashboard/people-counter/<str:url_hash>", people_counter, name="people_counter"
    ),
    path("dashboard/users/<str:url_hash>", users_list, name="users"),
    path("dashboard/generate-user/<str:url_hash>", generate_user, name="generate_user"),
    path(
        "dashboard/edit-user-permissions/<int:user_id>/",
        user_permissions,
        name="edit-user-permissions",
    ),
    path(
        "dashboard/edit-branch-permissions/<int:user_id>/",
        branch_permissions,
        name="edit-branch-permissions",
    ),
    path("dashboard/campaigns/<str:url_hash>", campaign, name="campaign"),
    path("dashboard/create-campaign/<str:url_hash>", create_campaign, name="create_campaign"),
    path("dashboard/edit-campaign/<int:campaign_id>", edit_campaign, name="edit_campaign"),
    path("dashboard/delete-campaign/<int:campaign_id>", delete_campaign, name='delete_campaign'),
    path("dashboard/campaign-solo-analysis/<int:campaign_id>", campaign_detail, name='campaign_solo_analysis'),
    path("dashboard/create-invoice-from-excel/<str:url_hash>", upload_excel_file_invoice, name='upload_excel_file_invoice'),
    path("dashboard/invoices/<str:url_hash>", invoices, name='invoices'),
    path("dashboard/invoices/invoice-detail/<int:invoice_pk>", invoice_detail, name='invoice_detail'),
    path("dashboard/invoice-delete/<int:invoice_pk>", invoice_delete, name='invoice_delete'),
    path("dashboard/excel-template-generator/<str:url_hash>", excel_template_generator, name='excel_template_generator'),
    path("dashboard/sales-counter/<str:url_hash>", invoice_counter, name='invoice_counter'),
    path("dashboard/analysis/<str:url_hash>", analysis, name='analysis'),
    path("dashboard/account/login", custom_login, name="login"),
    path(
        "dashboard/account/logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("dashboard/account/profile/<int:user_id>/", profile, name="profile"),
    path("dashboard/<str:url_hash>", home, name="home"),
    path("api/multi-branch-data", MultipleBranches.as_view(), name="multi_branch_data"),
    path("api/multi-branch-invoice-data", MultiBranchesInvoice.as_view(), name="multi_branch_invoice_data"),
    path("api/analysis", Analysis.as_view(), name="analysis"),
    path("api/get-campaign-each-point", GetCampaignEachPoint.as_view(), name="get_campaign_each_point"),
    path("test/", test, name="test"),
]
