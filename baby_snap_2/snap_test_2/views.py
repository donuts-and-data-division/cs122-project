from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations, FoodPrices
from django.core.serializers import serialize
from . import placesAPI as pa
from . import pricesAPI as pricesAPI
from django.contrib.gis.geos import Polygon
from django.contrib import messages
from .forms import SearchForm, PricesForm, GroceryForm
from .forms import SearchForm, FilterForm
from django.http import JsonResponse
#import simplejson as json

#def index(request):
#    return render(request, 'snap_test_2/index.html',{})

def index(request):
    qs_results = SnapLocations.objects.all()
    return render(request, "snap_test_2/index.html", 
        {"qs_results":qs_results})

def get_places(request):
    print("Roger. Getting places.")
    sw_lon = request.GET.get('sw_lon',None)
    sw_lat = request.GET.get('sw_lat',None)
    ne_lon = request.GET.get('ne_lon',None)
    ne_lat = request.GET.get('ne_lat',None)
    
    form_data = dict(request.GET)
    
    price_levels = []
    categories = []
    min_rating = 0
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
    #default lists for filters: include all
    if price_levels == []:
        price_levels = SnapLocations.objects.values_list('price_level').distinct() 
    if categories == []:
        categories = SnapLocations.objects.values_list('store_category').distinct() 
        
    print('price_levels: ', price_levels, 'categories: ', categories, 'min_rating: ', min_rating)
    viewport = pa.get_viewport_poly((sw_lon, sw_lat, ne_lon, ne_lat))
    data = {"data": serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport).filter(price_level__in = price_levels).filter(store_category__in = categories).filter(rating__gte = min_rating))}

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
    print("hello cash_register")
    food_id = request.GET.get('food_id', None)
    store_id = request.GET.get('store_id', None)
    price_estimate = pricesAPI.get_price_estimate(store_id,food_id)
    print(price_estimate)
    data = {
            'food_price': price_estimate,
            #'food_price': FoodPrices.objects.get(id=food_id).food_price,
            'food_quantity': FoodPrices.objects.get(id=food_id).food_quantity,
            'food_name': FoodPrices.objects.get(id=food_id).food_name
            }

    return JsonResponse(data)

def update_price(request):
    food_id = request.GET.get('food_id', None)
    store_id = request.GET.get('store_id', None)
    user_price = request.GET.get('user_price',None)

    pricesAPI.update_price_estimate(store_id,food_id,user_price)
    
    data = {"thanks": "thanks"}

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
        'store_name': store_name, 'address': store_address, 'food_list': food_id_list})


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
        'store_name': store_name, 'address': store_address, 'food_list': food_list})

