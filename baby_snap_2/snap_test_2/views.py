from django.shortcuts import render
from django.http import HttpResponse
from .models import SnapLocations
from django.core.serializers import serialize
from . import placesAPI
from django.contrib.gis.geos import Polygon

#def index(request):
#    return render(request, 'snap_test_2/index.html',{})

def index(request):
    qs_results = SnapLocations.objects.all()
    return render(request, "snap_test_2/index.html", 
        {"qs_results":qs_results})

def snapdata(request, key = "AIzaSyC-_IRZoDqHowcopoCBFvQFGG7wU9CNOPw"
):
    query = "Chicago, IL"
    geometry = placesAPI.get_geometry(query, key)
    sw_lat = geometry["viewport"]['southwest']['lat']
    sw_lon = geometry["viewport"]['southwest']['lng']
    ne_lat = geometry["viewport"]['northeast']['lat']
    ne_lon = geometry["viewport"]['northeast']['lng']

    viewport = Polygon.from_bbox((sw_lon, sw_lat, ne_lon, ne_lat))
    qs_geojson = serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport))

    return HttpResponse(qs_geojson, content_type='json')

def gmap(request):
    return render(request, "snap_test_2/gmap.html")

def prettygmap(request):
    return render(request, "snap_test_2/prettygmap.html")


"""### PROBABLY PUT IN DIFFERENT FILE
import requests



def get_geometry(query, key = KEY):
    r = requests.get(make_url(query, key))
    try:
        return r.json()["results"][0]["geometry"]
    except:        
        if r.status_code != 200:
            print("Error: failed request")
        elif r.json()["status"] != "OK": 
            print("Error: No such result")



def make_url(query, key = KEY):
    '''
    Inputs: query (string)
    Returns: url for text search 
    '''
    query = "+".join(query.split())
    return "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}".format(query,key)

"""