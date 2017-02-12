##Donuts-and-Data-Division
##code to connect database to Places IDs

import json
import pandas as pd
import requests
from time import sleep


def get_url(lat, lon, keyword, key):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
={},{}&keyword={}&radius=500&key=AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828".\
format(lat, lon, keyword, key)

    return url


IL_filename = "IL.csv"
IL = pd.read_csv(IL_filename)

developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828"]
key = developerKeys[0]

ids = []
lats = []
lngs = []
costs = []

for i in range(len(IL[:5])):
    address = IL.loc[i]["Address"] 
    keyword = address.split()[0]
    lat = IL.loc[i]["Latitude"]
    lon = IL.loc[i]["Longitude"]

    url = get_url(lat, lon, keyword, key)
    print (url)
    r = requests.get(url)
    json = r.json()
    print (json)

    if json["results"] == []:
        print ("oh no!")
        name = IL.loc[i]["Store_Name"]
        keyword = name.split()[0]
        #keyword = "+".join(name.split())
        url = get_url(lat, lon, keyword, key)
        print (url)
        r2 = requests.get(url)
        json = r2.json()

        
        if len(json["results"]) > 1:
            print ("more than one")

        if json["results"] == []:
            print ("oh no again!")


    
    #only works with one result
    ids.append(json["results"][0]["place_id"])
    lats.append(json["results"][0]["geometry"]["location"]["lat"])
    lngs.append(json["results"][0]["geometry"]["location"]["lng"])

    if "price_level" in json["results"][0]:
        costs.append(json["results"][0]["price_level"])
    #types.append(json["results"][0]["types"])

#creates new column and fills each row 
IL["googlelat"] = lats
IL["googlelon"] = lons
IL["place_id"] = ids
IL["cost"] = costs
#IL["type"] = types
#IL["hours"]



"""
def get_text_search_url(query, key):
    query = "+".join(query.split())

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}".format(query,key)
    return url
"""







"""
service = build ('places', 'something', developerKey = developerKey[1])
request = service. 
response = request.execute()
 

CREATE TABLE snap_retailers
(store_name,
longitude, 
latitude, 
Address,
Address2,
City, 
State, 
Zip5, 
Zip4, 
County, 
PRIMARY KEY (store_name));

.separator ,
.import IL2.csv snap_retailers
""" 