from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations
from django.core.serializers import serialize
from . import placesAPI
from django.contrib.gis.geos import Polygon
from django.contrib import messages
from .forms import SearchNearby
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
    #query = "Peoria, IL"
    #geometry = placesAPI.get_geometry(query, key)

    
    sw_lat = geometry["viewport"]['southwest']['lat']
    sw_lon = geometry["viewport"]['southwest']['lng']
    ne_lat = geometry["viewport"]['northeast']['lat']
    ne_lon = geometry["viewport"]['northeast']['lng']

    viewport = Polygon.from_bbox((sw_lon, sw_lat, ne_lon, ne_lat))
    qs_geojson = serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport))

    return render(request, "snap_test_2/geojson.html",  {"qs_geojson":qs_geojson})
    
def gmap(request):
    qs_results = SnapLocations.objects.all()
    qs_results = serialize('geojson', qs_results)
    
    return render(request, "snap_test_2/gmap.html", 
        {"qs_results":qs_results})



from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

class SignUpView(CreateView):
    template_name = 'snap_test_2/signup.html'
    form_class = UserCreationForm

from django.http import JsonResponse

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def gmapdata(request):
    qs_results = SnapLocations.objects.all()
    qs_results = serialize('geojson', qs_results)
    return HttpResponse(qs_results, content_type= 'json')

def auto(request):
    return render(request, 'snap_test_2/auto.html', {})


def search_retailers(request):
    if request.method == 'POST': # If the form has been submitted...
        location = SearchNearby(request.POST) # A form bound to the POST data   
    else:
        location = SearchNearby()
    # DO FILTERING HERE
    qs_results = SnapLocations.objects.values_list('googlename',  flat=True)
    return render(request, 'snap_test_2/gmap2.html', {'qs_results': qs_results, 'location': location})

    
def capture_loc(request):
    location = request.Get.get('location', None)
    return JsonResponse(location)


"""
def geoquery(request, key = "AIzaSyD2zsB1fPiX_9LUi7t_hyA_TaY3E2aAPQU"):
    query = "Chicago, IL"
    geometry = placesAPI.get_geometry(query, key)
    sw_lat = geometry["viewport"]['southwest']['lat']
    sw_lon = geometry["viewport"]['southwest']['lng']
    ne_lat = geometry["viewport"]['northeast']['lat']
    ne_lon = geometry["viewport"]['northeast']['lng']
    viewport = Polygon.from_bbox((sw_lon, sw_lat, ne_lon, ne_lat))
    snap_locations=SnapLocations.objects.filter(geom__contained = viewport))

"""


