from django.forms import ModelForm
from django.contrib.auth.models import User

class Generate_User(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email", "is_staff", "is_active"]

