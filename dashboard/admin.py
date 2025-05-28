from django.contrib import admin
from .models import PeopleCounting

# Register your models here.

class PeopleCountingAdmin(admin.ModelAdmin):
    list_display = ["date", "vendor", "branch", "entry"]
    list_filter = ["vendor", "branch", "date"]
    exclude = ["date"]

admin.site.register(PeopleCounting, PeopleCountingAdmin)
