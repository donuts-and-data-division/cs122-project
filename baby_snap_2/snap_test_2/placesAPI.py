# Get Address and bounding box
import requests

# I'm guessing what we call the database
from snap_test_2.models import SnapLocations
KEY = "AIzaSyC-_IRZoDqHowcopoCBFvQFGG7wU9CNOPw"


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


def get_nearby_locations(query, key = KEY):
    '''
    Constructs geographic query base on google API bounding box
    'SELECT * FROM db WHERE db.lat >= sw_lat AND db.lat <= ne_lat AND
     db.lon >= sw_lon AND db.lon <= ne_lon'
    ''' 
    geometry = get_geometry(query, key)
    sw_lat = geometry["viewport"]['southwest']['lat']
    sw_lon = geometry["viewport"]['southwest']['lng']
    ne_lat = geometry["viewport"]['northeast']['lat']
    ne_lon = geometry["viewport"]['northeast']['lng']

    return SnapLocations.objects.filter(lat__gt=sw_lat, lat__lt= ne_lat,\
     lon__gt=sw_lon, lon__lt= ne_lon)






