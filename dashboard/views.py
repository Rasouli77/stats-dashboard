from django.shortcuts import render
from .initial_data_entry import initial_entry
# Create your views here.

def people_counter(request):
    initial_entry()
    print('success')
    return render(request, "people-counter.html")


