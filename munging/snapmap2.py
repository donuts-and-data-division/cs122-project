##Donuts-and-Data-Division
##code to connect database to Places IDs

import json
import pandas as pd
import requests
from time import sleep
import recordlinkage as rl
import jellyfish
import backoff


#def get_url(lat, lon, keyword, radius, key):

    #url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
#={},{}&keyword={}&radius={}&key={}".format(lat, lon, keyword, radius, key)
    #return url

@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError, max_tries=3)
def get_place_url(lat, lon, keyword, radius, key):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
={},{}&keyword={}&radius={}&key={}".format(lat, lon, keyword, radius, key)
    print (url)
    r = requests.get(url)
    return r.json()

def get_place_details_url(placeid, key):
    url = "https://maps.googleapis.com/maps/api/place/details/json?\
placeid={}&key={}".format(placeid, key)
    print (url)
    r = requests.get(url)
    return r.json()

def get_info(num):
    IL_filename = "Snap_With_Markets.csv"
    #IL = pd.read_csv(IL_filename)
    df = pd.read_csv(IL_filename)
    IL = df[df["City"] == "Chicago"]
    IL.reset_index(drop = True, inplace = True)

    KEY_INDEX = 0
    developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828",\
    "AIzaSyBUDrUeEyJyUNwQl1oVJCydSFPb5fCMQvw", "AIzaSyC9dbLTJ-aU2VL0r1Zhpzlxx99TrW-tpMM",\
    "AIzaSyBkWTxpnmygafi2mFETLRumyw0OlY_ftwM", "AIzaSyC-_IRZoDqHowcopoCBFvQFGG7wU9CNOPw", \
    "AIzaSyDJUsXYFdat1urw-QLkvbZu17gmEj45its", "AIzaSyDef0qoVNWFiIhSf2DIcI6s393w2ikTj2E", \
    "AIzaSyBbj_MRDIQC-GiOLuttSbCyht4cG-CkSjU", "AIzaSyAHH7pVva_7a2Ue4kWVkIvJPoihOvGPdqY", \
    "AIzaSyAHH7pVva_7a2Ue4kWVkIvJPoihOvGPdqY", "AIzaSyC7ukvijmGEqmfRIPZiNlFsXS436eXJs18", \
    "AIzaSyCls1mcmSzQnNPbTjeYrLA8yyde4AsH0rU"]
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
    category = [0]*len(IL.index)
    types = [0]*len(IL.index)
    form_adds = [0]*len(IL.index)
    phone = [0]*len(IL.index)
    hours = [0]*len(IL.index)
    website = [0]*len(IL.index)
    url = [0]*len(IL.index)
    rating = [0]*len(IL.index)
    
    #typeset = set()
    completed = 0

    for i in range(len(IL[:num])):
        sleep(1)

        name = IL.loc[i]["Store_Name"]
        address = IL.loc[i]["Address"] 
        lat = IL.loc[i]["Latitude"]
        lon = IL.loc[i]["Longitude"]

        #specific search for Farmer's Market locations
        if IL.loc[i]["Farmers Market?"] == True:
            keyword = "Market"
        else:    
            keyword = address.split()[0]

        json = get_place_url(lat, lon, keyword, 200, key)
        multiple[i] = len(json["results"])
        how[i] = 'address first word'

        if json["status"] == "OVER_QUERY_LIMIT":
            KEY_INDEX += 1
            key = developerKeys[KEY_INDEX]
            json = get_place_url(lat, lon, keyword, 200, key)
            check[i] = "Changed Key"

        if len(json["results"]) > 1:
            print ("more than one")
            sleep(1.25)

            if IL.loc[i]["Farmers Market?"] == True:
                new_keyword = name.split()[0] + "Market" 
            else: 
                keyword0 = address.split()[0]
                keyword1 = name.split()[0]
                new_keyword = keyword0 + ' ' + keyword1

            json = get_place_url(lat, lon, new_keyword, 200, key)

            if json["status"] == "OVER_QUERY_LIMIT":
                KEY_INDEX += 1
                key = developerKeys[KEY_INDEX]
                json = get_place_url(lat, lon, new_keyword, 200, key)
                check[i] = "Changed Key"

            multiple[i] = len(json["results"])
            how[i] = 'name 1 and address 1 (more than one first) '


        if json["results"] == []:
            sleep(1.25)
            print ("oh no!") 
            keyword = name.split()[0]

            json = get_place_url(lat, lon, keyword, 300, key)

            if json["status"] == "OVER_QUERY_LIMIT":
                KEY_INDEX += 1
                key = developerKeys[KEY_INDEX]
                json = get_place_url(lat, lon, keyword, 300, key)
                check[i] = "Changed Key"

            multiple[i] = len(json["results"])
            how[i] = 'name first word'
            
            if len(json["results"]) > 1:
                print ("more than one")
                sleep(1.25)
                if len(name.split()) >= 2:
                    keyword0 = name.split()[0]
                    keyword1 = name.split()[1]
                    new_keyword = keyword0 + ' ' + keyword1
                    json = get_place_url(lat, lon, new_keyword, 200, key)

                else: 
                    json = get_place_url(lat, lon, keyword, 200, key)

                if json["status"] == "OVER_QUERY_LIMIT":
                    KEY_INDEX += 1
                    key = developerKeys[KEY_INDEX]
                    check[i] = "Changed Key"

                multiple[i] = len(json["results"])
                how[i] = 'name 1 & 2 (none first)'
        
        if json["results"] == []:
            sleep(1.25)
            print ("oh no again!")
            if len(name.split()) >= 2:
                keyword = name.split()[1]
                json = get_place_url(lat, lon, keyword, 300, key)

            else: 
                json = get_place_url(lat, lon, keyword, 400, key)

            if json["status"] == "OVER_QUERY_LIMIT":
                KEY_INDEX += 1
                key = developerKeys[KEY_INDEX]
                check[i] = "Changed Key"

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
            category[i] = "unkown"
            continue

        #check if googleaddress closely matches input address
        #firstthree = address.split()[0] + "" + address.split()[1] + "" + address.split()[2]
        #googfirstthree = json["results"][0]["vicinity"].split()[0] + "" + json["results"][0]["vicinity"].split()[1] \
        #+ "" + json["results"][0]["vicinity"].split()[2]

        add1 = address.split()[0]
        add2 = json["results"][0]["vicinity"].split()[0]

        #if len(address.split()) < 3 or len(json["results"][0]["vicinity"].split()) < 3:
            #add1 = address.split()[0] + address.split()[1] 
            #add2 = json["results"][0]["vicinity"].split()[0] + json["results"][0]["vicinity"].split()[1] 
        
        #if len(address.split()) > 3 and len(json["results"][0]["vicinity"].split()) >= 3: 
            #add1 = address.split()[0] + address.split()[1] + address.split()[2]
            #add2 = json["results"][0]["vicinity"].split()[0] + json["results"][0]["vicinity"].split()[1] + json["results"][0]["vicinity"].split()[2]
        
        if jellyfish.levenshtein_distance(add1.lower(), add2.lower()) > 0.5*len(add1):
            check[i] = "Double Check- Address mismatch"

        if multiple[i] > 5:
            check[i] = "Double Check- Many results"


        #will be accurate if one result
        ids[i] = json["results"][0]["place_id"]
        names[i] = json["results"][0]["name"]
        lats[i] = json["results"][0]["geometry"]["location"]["lat"]
        lngs[i] = json["results"][0]["geometry"]["location"]["lng"]
        adds[i] = json["results"][0]["vicinity"]
        if IL.loc[i]["Farmers Market?"] == True:
            category[i] = "Farmer's Market"
        else: 
            #category[i] = categorize(json["results"][0]["types"])
            category[i] = categorize(json)
        types[i] = json["results"][0]["types"]

        #if "restaurant" in json["results"][0]["types"]:
            #check[i] = "Double Check- invalid type"

        if "price_level" in json["results"][0]:
            costs[i] = json["results"][0]["price_level"]
        else:
            costs[i] = None
        

        #USE ID TO GET PLACES INFO
        add_d, phone_d, hours_d, website_d, url_d, rating_d = get_details_info(json["results"][0]["place_id"], key)
        form_adds[i] = add_d
        phone[i] = phone_d
        hours[i] = hours_d
        website[i] = website_d
        url[i] = url_d
        rating[i] = rating_d

        #typeset.add(tuple(json["results"][0]["types"]))
        completed += 1
        print (completed)

    #Add collected info to dataframe
    IL["place_id"] = ids
    IL["googlename"] = names
    IL["googlelat"] = lats
    IL["googlelon"] = lngs
    IL["googleaddress"] = adds
    IL["cost"] = costs
    IL['multiple'] = multiple
    IL['how'] = how
    IL['check'] = check
    IL["type"] = types
    IL["category"] = category
    IL["address"] = form_adds
    IL["phone number"] = phone
    IL["hours"] = hours
    IL["website"] = website
    IL["url"] = url
    IL["rating"] = rating
    
    #print(typeset)
    IL.to_csv("snapresultstestChicago1.csv")

def get_details_info(place_id, key):
    json = get_place_details_url(place_id, key)
    form_add = json["result"]["formatted_address"]
    if "formatted_phone_number" in json["result"]:
        phone = json["result"]["formatted_phone_number"]
    else:
        phone = "None"
    if "opening_hours" in json["result"]:
        hours = json["result"]["opening_hours"]["weekday_text"]
    else: 
        hours = "None"
    if "website" in json["result"]:
        website = json["result"]["website"]
    else:
        website = "None"
    url = json["result"]["url"]
    if "rating" in json["result"]:
        rating = json["result"]["rating"]
    else:
        rating = "None"
    return form_add, phone, hours, website, url, rating

"""
def get_details_info(i, place_id, key, forms_adds, phone, hours, website, url, rating):
    print (form_adds)
    json = get_place_details_url(place_id, key)

    form_adds[i] = json["result"]["formatted_address"]
    phone[i] = json["result"]["formatted_phone_number"]
    hours[i] = json["result"]["opening_hours"]["weekday_text"]
    if ["website"] in json["result"]:
        website[i] = json["result"]["website"]
    url[i] = json["result"]["url"]
    rating[i] = json["result"]["rating"]
"""
    
def categorize(json):
    types_list = json["results"][0]["types"]

    if "gas_station" in types_list: 
        category = "gas station"
    elif "convenience_store" in types_list or "liquor_store" in types_list:
        category = "convenience store"
    elif "grocery_or_supermarket" in types_list and "convenience_store" not in types_list:
        category = "grocery"
    elif "bakery" in types_list or "cafe" in types_list:
        category = "other"
    else:
        category = "other"

    return category

def best_result(json, name):
    best = 0
    for i in range(len(json["results"])):
        g_name = json["results"][i]["name"]
        print (g_name)
        if jellyfish.jaro_distance(json["results"][i]["name"], name) > best:
            best = i
    json = json["results"][i]

    return json









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
