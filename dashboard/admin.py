from django.contrib import admin
from .models import (
    PeopleCounting,
    Merchant,
    Cam,
    Country,
    Province,
    City,
    District,
    Branch,
    Campaign,
    UserProfile,
    PermissionToViewBranch,
    Invoice,
)
from rangefilter.filters import DateRangeFilter

# Register your models here.


class PeopleCountingAdmin(admin.ModelAdmin):
    list_display = (
        "merchant",
        "date",
        "branch",
        "cam",
        "entry",
        "exit",
        "date_created",
        "last_modified",
    )
    list_filter = ["branch", "date"]
    exclude = ["date_created"]


class CamAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "country",
        "province",
        "city",
        "district",
        "branch",
        "zone",
        "entry",
        "ip",
        "cam_name",
        "merchant",
    ]
    autocomplete_fields = [
        "country",
        "province",
        "city",
        "district",
        "branch",
        "merchant",
    ]
    exclude = ["date_created"]


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    exclude = ["date_created"]


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
    search_fields = ["name"]
    autocomplete_fields = ["country"]
    exclude = ["date_created"]


class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "province"]
    search_fields = ["name"]
    autocomplete_fields = ["province"]
    exclude = ["date_created"]


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "city"]
    search_fields = ["name"]
    autocomplete_fields = ["city"]
    exclude = ["date_created"]


class BranchAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "district", "merchant"]
    search_fields = ["name", "pk"]
    autocomplete_fields = ["district"]
    exclude = ["date_created"]


class CampaignCalendarAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "pk"]
    autocomplete_fields = ["branch"]
    exclude = ["date_created"]


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0


class MerchantAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "rep_first_name",
        "rep_last_name",
        "rep_mobile_number",
        "contract_start_date",
        "contract_expiration_date",
    ]
    search_fields = ["name"]
    exclude = ["date_created"]
    inlines = [UserProfileInline]


class PermissionToViewBranchAdmin(admin.ModelAdmin):
    list_display = ["user", "branch"]
    exclude = ["date_created"]
    autocomplete_fields = ["branch"]


class PermissionToViewBranchInline(admin.TabularInline):
    model = PermissionToViewBranch
    autocomplete_fields = ["branch"]
    extra = 0


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "merchant", "pk"]
    autocomplete_fields = ["merchant", "user"]
    inlines = [PermissionToViewBranchInline]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["date", "branch", "total_amount", "total_items"]
    autocomplete_fields = ["branch"]
    list_filter = ["branch", "date_created"]
    exclude = ["date_created"]
    list_per_page = 75


admin.site.register(PeopleCounting, PeopleCountingAdmin)
admin.site.register(Cam, CamAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Campaign, CampaignCalendarAdmin)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PermissionToViewBranch, PermissionToViewBranchAdmin)
admin.site.register(Invoice, InvoiceAdmin)
