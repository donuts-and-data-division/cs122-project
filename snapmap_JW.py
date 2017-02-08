import json
import pandas as pd
import requests
from time import sleep


def get_url(lat, lon, keyword, key, radius):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
={},{}&keyword={}&radius={}&key={}".\
format(lat, lon, keyword, radius,key)

    return url

def process(num):

    filename = "store_locations_IL.csv"
    IL = pd.read_csv(filename)

    developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828"]
    key = developerKeys[0]

    ids = [0]*len(IL.index)
    names= [0]*len(IL.index)
    lats = [0]*len(IL.index)
    lngs = [0]*len(IL.index)
    costs = [0]*len(IL.index)
    adds = [0]*len(IL.index)

    for i in range(len(IL[:num])):
        address = IL.loc[i]["Address"] 
        lat = IL.loc[i]["Latitude"]
        lon = IL.loc[i]["Longitude"]
        name = IL.loc[i]['Store_Name']

        first_word = name.split()[0]
        addr0 = address.split()[0]
        addr1 = address.split()[1]
        keywords = first_word + ' ' + addr0 + ' ' + addr1

        url = get_url(lat, lon, keywords, key, 300)
        r = requests.get(url)
        json = r.json()
        
        # try to reduce radius if more than one result
        if len(json['results'])>1:
            url = get_url(lat, lon, keywords, key, 150)
            r = requests.get(url)
            json = r.json()
        
        if len(json['results'])==0:
            ids[i]=None
            names[i]=None
            lats[i]=None
            lngs[i]=None
            adds[i]= None
        
        else: 
            # will return the first result if multiple
            ids[i]=json["results"][0]["place_id"]
            names[i]=json["results"][0]['name']
            lats[i]=json["results"][0]["geometry"]["location"]["lat"]
            lngs[i]=json["results"][0]["geometry"]["location"]["lng"]
            adds[i]=json["results"][0]['vicinity']
        
    IL["place_id"] = ids
    IL["googlename"] = names
    IL["googlelat"] = lats
    IL["googlelon"] = lngs
    IL['googleaddres'] = adds

    IL.to_csv('snap_results.csv')

    