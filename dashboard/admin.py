from django.contrib import admin
from .models import PeopleCounting, Merchant, Cam, Country, Province, City, District, Branch, CampaignCalendar, DefaultDate

# Register your models here.

class PeopleCountingAdmin(admin.ModelAdmin):
    list_display = ["merchant", "date", "branch", "cam", "entry", "exit"]
    list_filter = ["branch", "date"]
    exclude = ["date_created"]
    
class CamAdmin(admin.ModelAdmin):
    list_display = ["country", "province", "city", "district", "branch", "zone", "entry", "ip", "cam_name", "merchant"]
    autocomplete_fields = ["country", "province", "city", "district", "branch", "merchant"]
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
    list_display = ["name", "district", "merchant"]
    search_fields = ["name"]
    autocomplete_fields = ["district"]
    exclude = ["date_created"]

class CampaignCalendarAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date"]
    autocomplete_fields = ["branch"]
    exclude = ["date_created"]

class DefaultDateAdmin(admin.ModelAdmin):
    list_display = ["start_date", "end_date"]
    exclude = ["date_created"]

class MerchantAdmin(admin.ModelAdmin):
    list_display = ["name", "rep_first_name", "rep_last_name", "rep_mobile_number", "contract_start_date", "contract_expiration_date"]
    search_fields = ["name"]
    exclude = ["date_created"]

admin.site.register(PeopleCounting, PeopleCountingAdmin)
admin.site.register(Cam, CamAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Branch, BranchAdmin)
admin.site.register(CampaignCalendar, CampaignCalendarAdmin)
admin.site.register(DefaultDate, DefaultDateAdmin)
admin.site.register(Merchant, MerchantAdmin)
