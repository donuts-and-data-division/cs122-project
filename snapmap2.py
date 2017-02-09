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


def get_info(num):
    IL_filename = "store_locations_IL.csv"
    IL = pd.read_csv(IL_filename)

    developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828",\
    "AIzaSyBUDrUeEyJyUNwQl1oVJCydSFPb5fCMQvw", "AIzaSyC9dbLTJ-aU2VL0r1Zhpzlxx99TrW-tpMM",\
    "AIzaSyBkWTxpnmygafi2mFETLRumyw0OlY_ftwM"]
    key = developerKeys[3]

    ids = [0]*len(IL.index)
    names= [0]*len(IL.index)
    lats = [0]*len(IL.index)
    lngs = [0]*len(IL.index)
    costs = [0]*len(IL.index)
    adds = [0]*len(IL.index)
    multiple = [0]*len(IL.index)
    how = [0]*len(IL.index)

    for i in range(len(IL[:num])):
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
        
        multiple[i] = len(json["results"])
        how[i] = 'address first word'

       #  if len(json["results"]) > 1:
         #   print ("more than one")

        if len(json["results"]) > 1:
            print ("more than one")
            sleep(1)
            keyword0 = address.split()[0]
            keyword1 = name.split()[0]
            new_keyword = keyword0 + ' ' + keyword1
            url = get_url(lat, lon, new_keyword, 200, key)
            print(url)
            r = requests.get(url)
            json = r.json()

            multiple[i] = len(json["results"])
            how[i] = 'name first word and address first word'


        if json["results"] == []:
            sleep(1)
            print ("oh no!") 
            keyword = name.split()[0]
            url = get_url(lat, lon, keyword, 300, key)
            print (url)
            r = requests.get(url)
            json = r.json()

            multiple[i] = len(json["results"])
            how[i] = 'name first word'
            
            if len(json["results"]) > 1:
                print ("more than one")
                sleep(1)
                keyword0 = name.split()[0]
                keyword1 = name.split()[1]
                new_keyword = keyword0 + ' ' + keyword1
                url = get_url(lat, lon, new_keyword, 200, key)
                print(url)
                r = requests.get(url)
                json = r.json()

                multiple[i] = len(json["results"])
                how[i] = 'name first word and second word'
        
        if json["results"] == []:
            sleep(1)
            print ("oh no again!")
            keyword = name.split()[1]
            url = get_url(lat, lon, keyword, 300, key)
            print(url)
            r = requests.get(url)
            json = r.json()

            multiple[i] = len(json["results"])
            how[i] = 'name second word'

            if len(json["results"]) > 1:
                print ("more than one")

                multiple[i] = len(json["results"])
                how[i] = 'name second word, >1 results'
          

        if json["results"] == []:
            print("NOOO")
            ids[i]=None
            names[i]=None
            lats[i]=None
            lngs[i]=None
            adds[i]= None
            costs[i] = None
            continue

        #will be accurate if one results
        ids[i] = json["results"][0]["place_id"]
        names[i] = json["results"][0]["name"]
        lats[i] = json["results"][0]["geometry"]["location"]["lat"]
        lngs[i] = json["results"][0]["geometry"]["location"]["lng"]
        adds[i] = json["results"][0]["vicinity"]


        if "price_level" in json["results"][0]:
            costs[i] = json["results"][0]["price_level"]
        else:
            costs[i] = None
        #types.append(json["results"][0]["types"])

    #creates new column and fills each row 
    IL["place_id"] = ids
    IL["googlename"] = names
    IL["googlelat"] = lats
    IL["googlelon"] = lngs
    IL["googleaddress"] = adds
    IL["cost"] = costs
    IL['multiple'] = multiple
    IL['how'] = how

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