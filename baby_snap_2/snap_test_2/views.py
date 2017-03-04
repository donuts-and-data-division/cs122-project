from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations, FoodPrices
from django.core.serializers import serialize
from . import placesAPI as pa
from django.contrib.gis.geos import Polygon
from django.contrib import messages
from .forms import SearchForm, GroceriesForm, PricesForm, GroceryForm
from .forms import SearchForm, FilterForm
from django.http import JsonResponse

#def index(request):
#    return render(request, 'snap_test_2/index.html',{})

def index(request):
    qs_results = SnapLocations.objects.all()
    return render(request, "snap_test_2/index.html", 
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
    form = FilterForm()
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
    # put this in different view?!!

    return render(request, 'snap_test_2/auto2.html', {'form': form, 'qs_results': qs_results_ser})


def prices(request):
    if request.method == "POST":
        prices = PricesForm(request.POST)
    else:
        prices = PricesForm()
    return render(request, "snap_test_2/prices.html", {'prices': prices})


def groceries(request):
    data = {}
    if request.method == "POST":
        groceries = GroceriesForm(request.POST)
        if groceries.is_valid():
            name = groceries.cleaned_data['name']
            retailer_type = groceries.cleaned_data['retailer_type']
            price = groceries.cleaned_data['price']
            data = {'name': name, 'retailer_type': retailer_type, 'price': price}
    else:
        groceries = GroceriesForm()
    return render(request, "snap_test_2/grocery_list_2.html", {'groceries': groceries, 'data': data})


def submit_grocery_list(request):
    
    if request.method == "POST":
        form = GroceryForm(request.POST)     

    else:
        form = GroceryForm()

    #this view will actually be coming from the map part, and will redirect to the grocery list page
    #make a dictionary with dollar sign info and list of foods available at that type of store?
    #add that dictionary to the render thing
    #somehow edit the dropdown menu on the form based on the list of foods...

    return render(request, 'snap_test_2/grocery_list_2.html', {'form': form})


def cash_register(request):
    food_id = request.GET.get('food_id', None)
    data = {
            'food_price': FoodPrices.objects.get(id=food_id).food_price,
            'food_quantity': FoodPrices.objects.get(id=food_id).food_quantity,
            'food_name': FoodPrices.objects.get(id=food_id).food_name
            }

    #probably add dollar signs to this dictionary
    #e.g. 'dollar_sign': 1

    return JsonResponse(data)

def submit_prices(request):
    if request.method == "POST":
        form = GroceryForms(request.POST)
    else:
        form = GroceryForm()

    return render(request, 'snap_test_2/submit-prices.html', {'form': form})