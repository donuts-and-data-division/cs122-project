# Get Address and bounding box
import requests
from django.contrib.gis.geos import Polygon
from snap_test_2.models import SnapLocations
KEY = "AIzaSyC-_IRZoDqHowcopoCBFvQFGG7wU9CNOPw"

#https://maps.googleapis.com/maps/api/place/textsearch/json?query=hyde+park+Chicago+IL&key=AIzaSyC-_IRZoDqHowcopoCBFvQFGG7wU9CNOPw

def make_url(query, key = KEY):
    '''
    Inputs: query (string)
    Returns: url for text search 
    '''
    query = "+".join(query.split())
    return "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}".format(query,key)

def get_geometry(query, key = KEY):
    '''
    Using Googel Places API textsearch get "places_geometry"
    '''
    r = requests.get(make_url(query, key))
    try:
        return r.json()["results"][0]["geometry"]
    except:        
        if r.status_code != 200:
            print("Error: failed request")
        elif r.json()["status"] != "OK": 
            print("Error: No such result")

def get_viewport_poly(places_geometry, key = KEY):
    '''
    From inputs forms bounding box polygon for geoquerying.

    input: places_geometry (tuple of form (sw_lon, sw_lat, ne_lon, ne_lat) 
        or google API geometry dictionary of form of LatLngBoundsLiteral:
       
        places_geometry =  { south: 41.6443349, 
            west: -87.94026689999998, 
            north: 42.023131, 
            east: -87.524044 }


        places_geometry =  {
                            "location" : {
                               "lat" : 41.8781136,
                               "lng" : -87.6297982
                            },
                            "viewport" : {
                               "northeast" : {
                                  "lat" : 42.023131,
                                  "lng" : -87.52404399999999
                               },
                               "southwest" : {
                                  "lat" : 41.6443349,
                                  "lng" : -87.9402669
                               }
                            }
                        }


    return: Polygon
    '''
    if isinstance(places_geometry, tuple) and len(places_geometry)==4:
        geom = places_geometry
    elif isinstance(places_geometry, dict) and places_geometry.get("east",False):
        sw_lat = places_geometry['south']
        sw_lon = places_geometry['west']
        ne_lat = places_geometry['north']
        ne_lon = places_geometry['east']
        geom = (sw_lon, sw_lat, ne_lon, ne_lat)
    elif isinstance(places_geometry, dict):
        sw_lat = places_geometry["viewport"]['southwest']['lat']
        sw_lon = places_geometry["viewport"]['southwest']['lng']
        ne_lat = places_geometry["viewport"]['northeast']['lat']
        ne_lon = places_geometry["viewport"]['northeast']['lng']
        geom = (sw_lon, sw_lat, ne_lon, ne_lat)
    else:
        raise TypeError("places_geometry must be len-4 tuple or dictionary")

    return Polygon.from_bbox(geom)

def make_nearby_url(places_geometry, loc_type = "store", key = KEY):
    '''
    Inputs: query (string)
    Returns: url for text search 
    '''
    lat = places_geometry["location"]["lat"]
    lng = places_geometry["location"]["lng"]

    radius = 100

    return "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={},{}&radius={}&type={}&key={}"\
    .format(lat,lng,radius,loc_type,key)

def get_nearby(places_geometry, key = KEY):
    r = requests.get(make_nearby_url(places_geometry, key))
    if r.status_code == 200:
        return r.json()
    else:
        return "ERROR: {}".format(r.status_code)

if __name__=="__main__":
    places_geometry =  {
                            "location" : {
                               "lat" : 41.8781136,
                               "lng" : -87.6297982
                            },
                            "viewport" : {
                               "northeast" : {
                                  "lat" : 42.023131,
                                  "lng" : -87.52404399999999
                               },
                               "southwest" : {
                                  "lat" : 41.6443349,
                                  "lng" : -87.9402669
                               }
                            }
                        }

    #nearby_places =  get_nearby(places_geometry)
    #our_places = get_model_locations(places_geometry)