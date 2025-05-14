from django.contrib import admin
from .models import Stats

# Register your models here.

class StatsAdmin(admin.ModelAdmin):
    list_display = ["date", "vendor", "branch", "entry"]
    list_filter = ["vendor", "branch", "date"]

admin.site.register(Stats, StatsAdmin)
