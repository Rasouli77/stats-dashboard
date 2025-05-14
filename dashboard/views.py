from django.shortcuts import render
from datetime import datetime, timedelta
from .camera_data import get_camera_data
# Create your views here.

def people_counter(request):
    return render(request, "people-counter.html")


