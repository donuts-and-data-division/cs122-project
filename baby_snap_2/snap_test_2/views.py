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

def snapdata(request, key = "AIzaSyD2zsB1fPiX_9LUi7t_hyA_TaY3E2aAPQU"):
    query = "Chicago, IL"
    geometry = placesAPI.get_geometry(query, key)
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
    sw_lat = 40#geometry["viewport"]['southwest']['lat']
    sw_lon = -88#geometry["viewport"]['southwest']['lng']
    ne_lat = 42#geometry["viewport"]['northeast']['lat']
    ne_lon = -86#geometry["viewport"]['northeast']['lng']

    viewport = Polygon.from_bbox((sw_lon, sw_lat, ne_lon, ne_lat))
    qs_geojson = serialize('geojson',SnapLocations.objects.filter(geom__contained = viewport))

    return render(request, "snap_test_2/geojson.html", 
      {"qs_geojson":qs_geojson})
    
def gmap(request):
    qs_results = SnapLocations.objects.all()
    qs_results = serialize('geojson', qs_results)
    return render(request, "snap_test_2/gmap.html", 
        {"qs_results":qs_results})
