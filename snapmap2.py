##Donuts-and-Data-Division
##code to connect database to Places IDs

import json
import pandas as pd
import requests
from time import sleep


def get_url(lat, lon, keyword, radius, key):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
={},{}&keyword={}&radius=300&key=AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828".\
format(lat, lon, keyword, radius, key)

    return url


IL_filename = "IL.csv"
IL = pd.read_csv(IL_filename)

developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828","AIzaSyBUDrUeEyJyUNwQl1oVJCydSFPb5fCMQvw", "AIzaSyC9dbLTJ-aU2VL0r1Zhpzlxx99TrW-tpMM"]
key = developerKeys[2]

ids = []
lats = []
lngs = []
costs = []
countafter3 = 0

for i in range(len(IL[:100])):
    sleep(1)
    address = IL.loc[i]["Address"] 
    keyword = address.split()[0]
    lat = IL.loc[i]["Latitude"]
    lon = IL.loc[i]["Longitude"]
    url = get_url(lat, lon, keyword, 200, key)
    print (url)
    r = requests.get(url)
    json = r.json()
    #print (json)

    if len(json["results"]) > 1:
        print ("more than one")

    if json["results"] == []:
        print ("oh no!") 
        name = IL.loc[i]["Store_Name"]
        keyword = name.split()[0]
        #keyword = "+".join(name.split())
        url = get_url(lat, lon, keyword, 300, key)
        print (url)
        r2 = requests.get(url)
        json = r2.json()

        if len(json["results"]) > 1:
            print ("more than one")

        if json["results"] == []:
            print ("oh no again!")
            keyword = name.split()[1]
            url = get_url(lat, lon, keyword, 300, key)
            print(url)
            r3 = requests.get(url)
            json = r3.json()

            if json["results"] == []:
                print("NOOO")
                countafter3 += 1
                print (countafter3)
        

"""
    #only works with one result
    ids.append(json["results"][0]["place_id"])
    print (ids)
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


return IL
"""


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
 
""" 