from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations, FoodPrices
from django.core.serializers import serialize
from . import placesAPI as pa
from . import pricesAPI as pricesAPI
from django.contrib.gis.geos import Polygon
from django.contrib import messages
from .forms import PricesForm, GroceryForm, FilterForm
from django.http import JsonResponse


def home(request):
    '''
    home page
    '''
    form = FilterForm()
    return render(request, 'snap_test_2/home.html', {'form':form})

def get_places(request):
    '''
    filters places based on ajax call
    optional inputs: bounding box, filters on price level, retailer type and rating
    returns: query set with location information (lat/lon and details)
    '''
    sw_lon = request.GET.get('sw_lon',None)
    sw_lat = request.GET.get('sw_lat',None)
    ne_lon = request.GET.get('ne_lon',None)
    ne_lat = request.GET.get('ne_lat',None)
    
    form_data = dict(request.GET)
    
    price_levels = []
    categories = []
    min_rating = 0
    # extract form data from dictionary; unique formatting requires extra work
    for i in range(0,14):
        if form_data.get('data['+str(i)+'][name]') is not None:
            if form_data['data['+str(i)+'][name]'][0] == 'price':
                price_levels.append(form_data['data['+str(i)+'][value]'][0])
            elif form_data['data['+str(i)+'][name]'][0] == 'retailer_type':
                categories.append(form_data['data['+str(i)+'][value]'][0])
            elif form_data['data['+str(i)+'][name]'][0] == 'rating':
                rating = float(form_data['data['+str(i)+'][value]'][0])
                if rating > min_rating:
                    min_rating = rating
    # default lists for filters: include all
    if price_levels == []:
        price_levels = SnapLocations.objects.values_list('price_level').distinct() 
    if categories == []:
        categories = SnapLocations.objects.values_list('store_category').distinct() 
        
    viewport = pa.get_viewport_poly((sw_lon, sw_lat, ne_lon, ne_lat))
    data = {"data": serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport).filter(price_level__in = price_levels).filter(store_category__in = categories).filter(rating__gte = min_rating))}

    return JsonResponse(data)

def submit_grocery_list(request, store_id):

    if request.method == "POST":
        form = GroceryForm(request.POST)     
    else:
        form = GroceryForm()

    store_name = SnapLocations.objects.get(store_id=store_id)
    store_address = SnapLocations.objects.get(store_id=store_id).address

    return render(request, 'snap_test_2/grocery_list_2.html', {'form': form, \
        'store_name': store_name, 'address': store_address, 'store_id': store_id})

def cash_register(request):
    '''
    returns prices to ajax call 
    (input: food_id and store_id)
    '''
    food_id = request.GET.get('food_id', None)
    store_id = request.GET.get('store_id', None)
    price_estimate = pricesAPI.get_price_estimate(store_id,food_id)
    
    data = {
            'food_price': price_estimate,
            'food_quantity': FoodPrices.objects.get(id=food_id).food_quantity,
            'food_name': FoodPrices.objects.get(id=food_id).food_name
            }

    return JsonResponse(data)

def update_price(request):
    '''
    updates database prices based on user input 
    (input: food_id, store_id and a price)
    returns "out of bounds error" or False (0)
    '''
    food_id = request.GET.get('food_id', None)
    store_id = request.GET.get('store_id', None)
    user_price = request.GET.get('user_price',None)

    data = {'bounds_error': 0}

    if pricesAPI.update_price_estimate(store_id,food_id,user_price):
        data['bounds_error'] = 'out of bounds error'

    return JsonResponse(data)


def submit_prices(request, store_id, food_string=0):

    '''Assumption we have SnapLocation informtion'''

    if request.method == "POST":
        form = GroceryForms(request.POST)
    else:
        form = GroceryForm()

    store_name = SnapLocations.objects.get(store_id=store_id)
    store_address = SnapLocations.objects.get(store_id=store_id).address
    food_id_list = food_string.split('&')
    food_list = []

    for food_id in food_id_list:
        food = FoodPrices.objects.get(id=food_id).food_name
        food_list.append(food)


    return render(request, 'snap_test_2/submit-prices.html', {'form': form, \
        'store_name': store_name, 'address': store_address, 'food_list': food_id_list, 'store_id': store_id})


def submit_prices_blank(request, store_id):

    '''Assumption we have SnapLocation informtion'''

    if request.method == "POST":
        form = GroceryForms(request.POST)
    else:
        form = GroceryForm()

    store_name = SnapLocations.objects.get(store_id=store_id)
    store_address = SnapLocations.objects.get(store_id=store_id).address
    food_list = []

    return render(request, 'snap_test_2/submit-prices.html', {'form': form, \
        'store_name': store_name, 'address': store_address, 'food_list': food_list, 'store_id': store_id})

