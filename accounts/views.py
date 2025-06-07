from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

# Create your views here.

def custom_login(request):
    if request.user.is_authenticated:
        print(request.user.pk)
        return redirect(reverse("home", args=[request.user.profile.merchant.url_hash]))
        
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("home", args=[request.user.profile.merchant.url_hash]))
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})
