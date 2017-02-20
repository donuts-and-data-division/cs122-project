from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations

#def index(request):
#    return render(request, 'snap_test_2/index.html',{})

def index(request):
    qs_results = SnapLocations.objects.all()
    return render(request, "snap_test_2/index.html", 
        {"qs_results":qs_results})

def gmap(request):
    qs_results = SnapLocations.objects.all()
    return render(request, "snap_test_2/gmap.html", 
        {"qs_results":qs_results})
