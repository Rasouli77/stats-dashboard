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
from django.urls import path
from dashboard.views import people_counter, users_list, generate_user, user_permissions, calender

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/people-counter/', people_counter, name="people_counter"),
    path('dashboard/users/', users_list, name="users"),
    path('dashboard/generate-user/', generate_user, name="generate_user"),
    path('dashboard/user-permissions/<int:user_id>/', user_permissions, name="user-permissions"),
    path('dashboard/calendar', calender, name="calendar"),
]
