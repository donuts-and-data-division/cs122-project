from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations
from django.core.serializers import serialize
from . import placesAPI as pa
from django.contrib.gis.geos import Polygon
from django.contrib import messages
from .forms import SearchForm
from django.http import JsonResponse

#def index(request):
#    return render(request, 'snap_test_2/index.html',{})

def index(request):
    qs_results = SnapLocations.objects.all()
    return render(request, "snap_test_2/index.html", 
        {"qs_results":qs_results})

def snapdata(request, key = "AIzaSyD2zsB1fPiX_9LUi7t_hyA_TaY3E2aAPQU"):
    #query = "Chicago, IL"
    #geometry = placesAPI.get_geometry(query, key)

    geometry =  {
                            "location" : {
                               "lat" : 41.8781136,
                               "lng" : -87.6297982
                            },
                            "viewport" : {
                               "northeast" : {
                                  "lat" : 50.023131,
                                  "lng" : -82.02404399999999
                               },
                               "southwest" : {
                                  "lat" : 39.6443349,
                                  "lng" : -98.9402669
                               }
                            }
                        }

    sw_lat = geometry["viewport"]['southwest']['lat']
    sw_lon = geometry["viewport"]['southwest']['lng']
    ne_lat = geometry["viewport"]['northeast']['lat']
    ne_lon = geometry["viewport"]['northeast']['lng']

    viewport = Polygon.from_bbox((sw_lon, sw_lat, ne_lon, ne_lat))
    qs_geojson = serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport))

    return HttpResponse(qs_geojson, content_type='json')
    #return render(request, "snap_test_2/gmap.html", 
        #{"qs_geojson":qs_geojson})

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
    place_name = request.GET.get("name", None)
    bounds = pa.get_geometry(place_name) #Relies on API
    viewport = pa.get_viewport_poly(bounds)
    data = {"data": serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport))}
    return JsonResponse(data)

def gmapdata(request):
    qs_results = SnapLocations.objects.all()
    qs_results = serialize('geojson', qs_results)
    return HttpResponse(qs_results, content_type= 'json')

#def auto(request):
 #   return render(request, 'snap_test_2/auto.html', {})


def auto2(request):
    qs_results = {}
    qs_results = serialize('geojson', qs_results)
    
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
            qs_results = serialize('geojson', qs_results)
    else:
        form = SearchForm()
        
    return render(request, 'snap_test_2/auto2.html', {'form': form, 'qs_results': qs_results})


