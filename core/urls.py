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
    campaign_detail,
    campaign_comparison,
    holiday_spotter,
    camera_list,
    alert_menu,
    alert_form_sms,
    alert_from_sms_contact_list,
    alert_from_sms_contact_list_detail,
    alert_form_social,
    alert_form_sms_edit,
    grouped_campaign_search_as_type,
    single_campaign_search_as_type
)
from dashboard.api_views import (
    MultipleBranches,
    MultiBranchesInvoice,
    Analysis,
    GetCampaignEachPoint,
    GroupedCampaigns,
    GroupedCampaignComparison,
    CampaignComparison,
    HolidaySpotter,
    CamStatus,
    NormalWeeklyDisplay,
    NormalMonthlyDisplay,
    abNormalWeeklyDisplay,
    abNormalMonthlyDisplay,
    AI
)
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.site.site_header = "پنل مدیریت اسپات لاین"
admin.site.site_title = "پنل مدیریت اسپات لاین"
admin.site.index_title = "پنل مدیریت اسپات لاین"


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
    path("dashboard/campaign-comparison/<str:url_hash>", campaign_comparison, name="campaign_comparison"),
    path(
        "dashboard/create-campaign/<str:url_hash>",
        create_campaign,
        name="create_campaign",
    ),
    path(
        "dashboard/edit-campaign/<str:url_hash>/<uuid:group_id>",
        edit_campaign,
        name="edit_campaign",
    ),
    path(
        "dashboard/delete-campaign/<str:url_hash>/<uuid:group_id>",
        delete_campaign,
        name="delete_campaign",
    ),
    path(
        "dashboard/campaign-solo-analysis/<int:campaign_id>",
        campaign_detail,
        name="campaign_solo_analysis",
    ),
    path(
        "dashboard/create-invoice-from-excel/<str:url_hash>",
        upload_excel_file_invoice,
        name="upload_excel_file_invoice",
    ),
    path("dashboard/invoices/<str:url_hash>", invoices, name="invoices"),
    path(
        "dashboard/invoices/invoice-detail/<int:invoice_pk>",
        invoice_detail,
        name="invoice_detail",
    ),
    path(
        "dashboard/invoice-delete/<int:invoice_pk>",
        invoice_delete,
        name="invoice_delete",
    ),
    path(
        "dashboard/excel-template-generator/<str:url_hash>",
        excel_template_generator,
        name="excel_template_generator",
    ),
    path(
        "dashboard/sales-counter/<str:url_hash>",
        invoice_counter,
        name="invoice_counter",
    ),
    path("dashboard/analysis/<str:url_hash>", analysis, name="analysis"),
    path("dashboard/account/login", custom_login, name="login"),
    path(
        "dashboard/account/logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("dashboard/account/profile/<int:user_id>/", profile, name="profile"),
    path("dashboard/<str:url_hash>", home, name="home"),
    path("api/multi-branch-data", MultipleBranches.as_view(), name="multi_branch_data"),
    path(
        "api/multi-branch-invoice-data",
        MultiBranchesInvoice.as_view(),
        name="multi_branch_invoice_data",
    ),
    path("api/analysis", Analysis.as_view(), name="analysis"),
    path(
        "api/get-campaign-each-point",
        GetCampaignEachPoint.as_view(),
        name="get_campaign_each_point",
    ),
    path("api/grouped-campaigns", GroupedCampaigns.as_view(), name="grouped_campaigns"),
    path("api/grouped-campaigns-comparison", GroupedCampaignComparison.as_view(), name="grouped_campaigns_comparison"),
    path("api/single-campaigns-comparison", CampaignComparison.as_view(), name="campaigns_comparison"),
    path("dashboard/camera-list/<str:url_hash>", camera_list, name="camera_list"), 
    path("api/holiday-spotter/<str:year>/<str:month>/<str:day>/", holiday_spotter, name="holiday_spotter"),
    path("api/holiday-spot", HolidaySpotter.as_view(), name="holiday_spot"),
    path("api/cam-status", CamStatus.as_view(), name="cam_status"),
    path("api/normal-weekly-display", NormalWeeklyDisplay.as_view(), name="normal-weekly-display"),
    path("api/normal-monthly-display", NormalMonthlyDisplay.as_view(), name="normal-monthly-display"),
    path("api/abnormal-weekly-display", abNormalWeeklyDisplay.as_view(), name="abnormal-weekly-display"),
    path("api/abnormal-monthly-display", abNormalMonthlyDisplay.as_view(), name="abnormal-monthly-display"),
    path("api/ai", AI.as_view(), name='ai'),
    path("dashboard/alert-menu/<str:url_hash>", alert_menu, name="alert_menu"),
    path("dashboard/alert-form-sms/<str:url_hash>", alert_form_sms, name="alert_form_sms"),
    path("dahsboard/alert-form-social/<str:url_hash>", alert_form_social, name="alert_form_social"),
    path("dashboard/alert-from-sms-contact-list/<str:url_hash>", alert_from_sms_contact_list, name="alert-from-sms-contact-list"),
    path("dashboard/alert-from-sms-contact-list-detail/<int:contact_id>", alert_from_sms_contact_list_detail, name="alert-from-sms-contact-list-detail"),
    path("dashboard/alert-form-sms-edit/<int:contact_id>", alert_form_sms_edit, name="alert-form-sms-edit"),
    path("dashboard/search/grouped-campaign-search-as-type/", grouped_campaign_search_as_type, name="grouped_campaign_search_as_type"),
    path("dashboard/search/single-campaign-search-as-type/", single_campaign_search_as_type, name="single_campaign_search_as_type"),
]
