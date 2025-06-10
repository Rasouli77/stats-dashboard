from django import forms
from django.contrib.auth.models import User, Permission


class Generate_User(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "is_staff",
            "is_active",
        ]

class UserPermissions(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().exclude(
            content_type__model__in=["session", "admin", "contenttype", "country", "province", "cam", "city", "district", "merchant", "logentry", "group", "branch", "permissiontoviewbranch", "user", "permission", "campaign", "defaultdate", "userprofile", "stats", "peoplecounting"]
        ),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label = "دسترسی ها"
    )
    class Meta:
        model = User
        fields = ["user_permissions"]