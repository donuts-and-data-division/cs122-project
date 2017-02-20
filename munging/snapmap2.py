##Donuts-and-Data-Division
##code to connect database to Places IDs

import json
import pandas as pd
import requests
from time import sleep
import recordlinkage as rl
import jellyfish


def get_url(lat, lon, keyword, radius, key):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
={},{}&keyword={}&radius={}&key={}".format(lat, lon, keyword, radius, key)

    return url


def get_info(num):
    #IL_filename = "store_locations_IL.csv"
    IL_filename = "Snap_With_Markets_sorted.csv"
    IL = pd.read_csv(IL_filename)

    KEY_INDEX = 1
    developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828",\
    "AIzaSyBUDrUeEyJyUNwQl1oVJCydSFPb5fCMQvw", "AIzaSyC9dbLTJ-aU2VL0r1Zhpzlxx99TrW-tpMM",\
    "AIzaSyBkWTxpnmygafi2mFETLRumyw0OlY_ftwM", "AIzaSyC-_IRZoDqHowcopoCBFvQFGG7wU9CNOPw"]
    key = developerKeys[KEY_INDEX]

    ids = [0]*len(IL.index)
    names= [0]*len(IL.index)
    lats = [0]*len(IL.index)
    lngs = [0]*len(IL.index)
    costs = [0]*len(IL.index)
    adds = [0]*len(IL.index)
    multiple = [0]*len(IL.index)
    how = [0]*len(IL.index)
    check = [0]*len(IL.index)


    for i in range(len(IL[:num])):
        sleep(1)

        name = IL.loc[i]["Store_Name"]
        address = IL.loc[i]["Address"] 
        lat = IL.loc[i]["Latitude"]
        lon = IL.loc[i]["Longitude"]

        #specific search for Farmer's Market category
        if IL.loc[i]["Farmers Market?"] == True:
            keyword = "Market"
        else:    
            keyword = address.split()[0]

        url = get_url(lat, lon, keyword, 200, key)
        print (url)
        r = requests.get(url)
        json = r.json()
        
        multiple[i] = len(json["results"])
        how[i] = 'address first word'

        if json["status"] == "OVER QUERY LIMIT":
            KEY_INDEX += 1
            key = developerKeys[KEY_INDEX]


       #  if len(json["results"]) > 1:
         #   print ("more than one")

        if len(json["results"]) > 1:
            print ("more than one")
            sleep(1)
            if IL.loc[i]["Farmers Market?"] == True:
                new_keyword = name.split()[0] + "Market" 
            else: 
                keyword0 = address.split()[0]
                keyword1 = name.split()[0]
                new_keyword = keyword0 + ' ' + keyword1
            url = get_url(lat, lon, new_keyword, 200, key)
            print(url)
            r = requests.get(url)
            json = r.json()

            multiple[i] = len(json["results"])
            how[i] = 'name 1 and address 1 (more than one first) '


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
                how[i] = 'name 1 & 2 (none first)'
        
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

        #check if googleaddress closely matches input address
        #firstthree = address.split()[0] + "" + address.split()[1] + "" + address.split()[2]
        #googfirstthree = json["results"][0]["vicinity"].split()[0] + "" + json["results"][0]["vicinity"].split()[1] \
        #+ "" + json["results"][0]["vicinity"].split()[2]

        add1 = address.split()[0]
        add2 = json["results"][0]["vicinity"].split()[0]

        if len(address.split()) < 3 or len(json["results"][0]["vicinity"].split()) < 3:
            add1 = address.split()[0] + address.split()[1] 
            add2 = json["results"][0]["vicinity"].split()[0] + json["results"][0]["vicinity"].split()[1] 
        
        if len(address.split()) > 3 and len(json["results"][0]["vicinity"].split()) >= 3: 
            add1 = address.split()[0] + address.split()[1] + address.split()[2]
            add2 = json["results"][0]["vicinity"].split()[0] + json["results"][0]["vicinity"].split()[1] + json["results"][0]["vicinity"].split()[2]
        
        if jellyfish.levenshtein_distance(add1.lower(), add2.lower()) > 0.5*len(add1):
            check[i] = "Double Check- Address mismatch"


        #will be accurate if one result
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
    IL['check'] = check

    #IL["type"] = types

    #return IL
    IL.to_csv("snapresultstestmarket.csv")


"""
#make recordlinkage dataframe from more than one result
dict = {"place_id":[], "googlename": [], "googlelat": [], "googlelon":[], \
"googleaddress": []}

for i in range(len(json["results"])):  
    dict["place_id"].append(json["results"][i]["place_id"])
    dict["googlename"].append(json["results"][i]["name"])
    dict["googlelat"].append(json["results"][i]["geometry"]["location"]["lat"])
    dict["googlelon"].append(json["results"][i]["geometry"]["location"]["lng"])
    dict["googleaddress"].append(json["results"][i]["vicinity"])
    #dict["cost"].append(json["results"][i]["price_level"])

#after running through urls
possible_matches_df = pd.DataFrame(dict)
#try to find matches




"""
"""
def get_text_search_url(query, key):
    query = "+".join(query.split())

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}".format(query,key)
    return url


service = build ('places', 'something', developerKey = developerKey[1])
request = service. 
response = request.execute()
 
""" 