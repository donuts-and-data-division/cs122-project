from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations
from django.core.serializers import serialize
from . import placesAPI as pa
from django.contrib.gis.geos import Polygon
from django.contrib import messages
from .forms import SearchForm, GroceriesForm, PricesForm
from .tables import ResultsTable
from django.http import JsonResponse
from django_tables2 import RequestConfig

#def index(request):
#    return render(request, 'snap_test_2/index.html',{})

def index(request):
    qs_results = SnapLocations.objects.all()
    return render(request, "snap_test_2/index.html", 
        {"qs_results":qs_results})


def prettygmap(request):
    return render(request, "snap_test_2/prettygmap.html")

def geojs(request, key = "AIzaSyD2zsB1fPiX_9LUi7t_hyA_TaY3E2aAPQU"):

    return render(request, "snap_test_2/geojson.html",  {"qs_geojson":qs_geojson})
    
def gmap(request):
    qs_results = SnapLocations.objects.all()
    qs_results = serialize('geojson', qs_results)

    return render(request, "snap_test_2/gmap.html", 
        {"qs_results":qs_results})


def get_places(request):
    #place_name = request.GET.get("name", None)
    #bounds = pa.get_geometry(place_name) #Relies on API
    sw_lon = request.GET.get('sw_lon',None)
    sw_lat = request.GET.get('sw_lat',None)
    ne_lon = request.GET.get('ne_lon',None)
    ne_lat = request.GET.get('ne_lat',None)

    viewport = pa.get_viewport_poly((sw_lon, sw_lat, ne_lon, ne_lat))
    data = {"data": serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport))}
    return JsonResponse(data)

def gmapdata(request):
    qs_results = SnapLocations.objects.all()
    qs_results = serialize('geojson', qs_results)
    return HttpResponse(qs_results, content_type= 'json')

def auto(request):
    form = SearchForm()
    return render(request, 'snap_test_2/auto.html', {'form':form})

def auto2(request):
    qs_results = {}
    qs_results_ser = serialize('geojson', qs_results)
    
    if request.method == 'POST': 
        form = SearchForm(request.POST)        
        if form.is_valid():
            location = form.cleaned_data['location']
            retailer_type = form.cleaned_data['retailer_type']
            price = form.cleaned_data['price']
            radius = form.cleaned_data['radius']
            sw_lat = form.cleaned_data['sw_lat']
            sw_lon = form.cleaned_data['sw_lon']
            ne_lat = form.cleaned_data['ne_lat']
            ne_lon = form.cleaned_data['ne_lon']
            
            viewport = pa.get_viewport_poly((sw_lon, sw_lat, ne_lon, ne_lat))
            #qs_results = SnapLocations.objects.filter(=price).filter(=retailer_type)
            # fill in filters with model fields after jazz updates
            qs_results = SnapLocations.objects.filter(geom__contained = viewport)
            qs_results_ser = serialize('geojson', qs_results)
    else:
        form = SearchForm()
    
    table = ResultsTable(qs_results)
    RequestConfig(request).configure(table)
    return render(request, 'snap_test_2/auto2.html', {'table': table, 'form': form, 'qs_results': qs_results_ser})


def prices(request):
    if request.method == "POST":
        prices = PricesForm(request.POST)
    else:
        prices = PricesForm()
    return render(request, "snap_test_2/prices.html", {'prices': prices})


def groceries(request):
    if request.method == "POST":
        groceries = GroceriesForm(request.POST)
        if groceries.is_valid():
            name = groceries.cleaned_data['name']
            retailer_type = groceries.cleaned_data['retailer_type']
            price = groceries.cleaned_data['price']
    else:
        groceries = GroceriesForm()
    return render(request, "snap_test_2/groceries.html", {'groceries': groceries})


