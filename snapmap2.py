##Donuts-and-Data-Division
##code to connect database to Places IDs

import json
import pandas as pd
import requests
from time import sleep


def get_url(lat, lon, keyword, radius, key):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
={},{}&keyword={}&radius={}&key={}".format(lat, lon, keyword, radius, key)

    return url


def get_info():
    IL_filename = "IL-100.csv"
    IL = pd.read_csv(IL_filename)

    developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828",\
    "AIzaSyBUDrUeEyJyUNwQl1oVJCydSFPb5fCMQvw", "AIzaSyC9dbLTJ-aU2VL0r1Zhpzlxx99TrW-tpMM",\
    "AIzaSyBkWTxpnmygafi2mFETLRumyw0OlY_ftwM"]
    key = developerKeys[3]

    ids = []
    names = []
    lats = []
    lngs = []
    costs = []
    adds = []

    for i in range(len(IL[:100])):
        sleep(1)
        name = IL.loc[i]["Store_Name"]
        address = IL.loc[i]["Address"] 
        lat = IL.loc[i]["Latitude"]
        lon = IL.loc[i]["Longitude"]

        keyword = address.split()[0]
        url = get_url(lat, lon, keyword, 200, key)
        print (url)
        r = requests.get(url)
        json = r.json()
        #print (json)

        if len(json["results"]) > 1:
            sleep(1)
            print ("more than one")

        if json["results"] == []:
            sleep(1)
            print ("oh no!") 
            keyword = name.split()[0]
            url = get_url(lat, lon, keyword, 300, key)
            print (url)
            r = requests.get(url)
            json = r.json()

            if len(json["results"]) > 1:
                sleep(1)
                print ("more than one")

            if json["results"] == []:
                sleep(1)
                print ("oh no again!")
                keyword = name.split()[1]
                url = get_url(lat, lon, keyword, 300, key)
                print(url)
                r = requests.get(url)
                json = r.json()

                if json["results"] == []:
                    print("NOOO")
                    ids.append("None")
                    names.append("None")
                    lats.append("None")
                    lngs.append("None")
                    adds.append("None")
                    costs.append("None")
                    continue

        #will be accurate if one results
        ids.append(json["results"][0]["place_id"])
        names.append(json["results"][0]["name"])
        lats.append(json["results"][0]["geometry"]["location"]["lat"])
        lngs.append(json["results"][0]["geometry"]["location"]["lng"])
        adds.append(json["results"][0]["vicinity"])


        if "price_level" in json["results"][0]:
            costs.append(json["results"][0]["price_level"])
        else:
            costs.append("None")
        #types.append(json["results"][0]["types"])

    #creates new column and fills each row 
    IL["place_id"] = ids
    IL["googlename"] = names
    IL["googlelat"] = lats
    IL["googlelon"] = lngs
    IL["googleaddress"] = adds
    IL["cost"] = costs

    #IL["type"] = types

    #return IL
    IL.to_csv("snapresults.csv")



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