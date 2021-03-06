##Donuts-and-Data-Division
##code to connect database to Places IDs

import json
import pandas as pd
import requests
from time import sleep
import recordlinkage as rl
import jellyfish
import backoff
import string
import re


def get_info(num, filename):
    """
    From USDA data, creates dataframe with all SNAP retailers in Chicago and adds 
    information from Google and Yelp APIs, when available. 

    Inputs: num (integer), number of rows to collect information for 
    Returns:  None; writes created dataframe to CSV. 
    """
    
    IL_filename = "Snap_With_Markets.csv"
    #IL = pd.read_csv(IL_filename)
    df = pd.read_csv(IL_filename)
    IL = df[df["City"] == "Chicago"]
    IL.reset_index(drop = True, inplace = True)

    headers = get_yelp_keys()

    KEY_INDEX = 0
    developerKeys = ["AIzaSyBiTMni2hEjQCIkmq8wVjyqBda2ZGgpTwg", "AIzaSyC0D12kQSiYdc0oioMEKMXJfR-QPALhzYQ"\
    "AIzaSyBytEe914saHxkWTfI71kqbVINrg2RWMhE", "AIzaSyBZiNslXrtBSQe75scT7K1Mb0pmyxIGM2M", \
    "AIzaSyA99nqCOeT0ouZkmlIl89Ysl-8l5Su67SY", "AIzaSyCBAgvlKZoVQ9TYzizDA21aNvmk3z5BgLc", \
     "AIzaSyDb7c1qkijqhCmmyciGEGeKEMRrZHRHYQQ", "AIzaSyBQdC9NUR0qPj1T0PY4OfgVm49GpaZsVCU", \
     "AIzaSyCls1mcmSzQnNPbTjeYrLA8yyde4AsH0rU", "AIzaSyC7ukvijmGEqmfRIPZiNlFsXS436eXJs18", \
     "AIzaSyAGADuJIZhQkgy8kZJ8KRNTclFVHvTB5CM", "AIzaSyAHH7pVva_7a2Ue4kWVkIvJPoihOvGPdqY", \
     "AIzaSyBbj_MRDIQC-GiOLuttSbCyht4cG-CkSjU", "AIzaSyDef0qoVNWFiIhSf2DIcI6s393w2ikTj2E", \
     "AIzaSyDJUsXYFdat1urw-QLkvbZu17gmEj45its"]
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
    price_level = [0]*len(IL.index)
    yelp_prices = [0]*len(IL.index)
    jaro = [0]*len(IL.index)
    
    #completed = 0
    for i in range(len(IL[:num])):
        sleep(1)

        name = IL.loc[i]["Store_Name"]
        address = IL.loc[i]["Address"] 
        lat = IL.loc[i]["Latitude"]
        lon = IL.loc[i]["Longitude"]

        #specific search term for Farmer's Market locations
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
            #print ("more than one")
            sleep(1.25)
            json["results"][0] = best_result(json, name)

            #these are extra calls to Google, currently using best_result instead
            """
            if IL.loc[i]["Farmers Market?"] == True:
                new_keyword = name.split()[0] + "Market" 
            else: 
                keyword0 = address.split()[0]
                keyword1 = name.split()[0]
                new_keyword = keyword0 + ' ' + keyword1

            json = get_place_url(lat, lon, new_keyword, 200, key)
            """
            
            if json["status"] == "OVER_QUERY_LIMIT":
                KEY_INDEX += 1
                key = developerKeys[KEY_INDEX]
                json["results"][0] = best_result(json, name)
                #json = get_place_url(lat, lon, new_keyword, 200, key)
                check[i] = "Changed Key"

            multiple[i] = len(json["results"])
            how[i] = 'name 1 and address 1 (more than one first) '


        if json["results"] == []:
            sleep(1.25)
            #print ("oh no!") 
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
                #print ("more than one")
                sleep(1.25)
                json["results"][0] = best_result(json, name)

                """
                if len(name.split()) >= 2:
                    keyword0 = name.split()[0]
                    keyword1 = name.split()[1]
                    new_keyword = keyword0 + ' ' + keyword1
                    json = get_place_url(lat, lon, new_keyword, 200, key)

                else: 
                    json = get_place_url(lat, lon, keyword, 200, key)
                """

                if json["status"] == "OVER_QUERY_LIMIT":
                    KEY_INDEX += 1
                    key = developerKeys[KEY_INDEX]
                    json["results"][0] = best_result(json, name)
                    check[i] = "Changed Key"

                multiple[i] = len(json["results"])
                how[i] = 'name 1 & 2 (none first)'
        
        if json["results"] == []:
            sleep(1.25)
            #print ("oh no again!")
            if len(name.split()) >= 2:
                keyword = name.split()[1]
                json = get_place_url(lat, lon, keyword, 300, key)

            else: 
                json = get_place_url(lat, lon, keyword, 400, key)

            if json["status"] == "OVER_QUERY_LIMIT":
                KEY_INDEX += 1
                key = developerKeys[KEY_INDEX]
                if len(name.split()) >= 2:
                    json = get_place_url(lat, lon, keyword, 300, key)
                else: 
                    json = get_place_url(lat, lon, keyword, 400, key)
                check[i] = "Changed Key"

            multiple[i] = len(json["results"])
            how[i] = 'name second word'

            if len(json["results"]) > 1:
                #print ("more than one")
                json["results"][0] = best_result(json, name)

                multiple[i] = len(json["results"])
                how[i] = 'name second word, >1 results'
          
        if json["results"] == []:
            #print("NOOO")
            ids[i]=None
            names[i]=None
            lats[i]=None
            lngs[i]=None
            adds[i]= None
            form_adds[i] = None
            phone[i] = None
            hours[i] = None
            website[i] = None
            url[i] = None
            rating[i] = None
            costs[i] = None
            price_level[i] = None
            yelp_prices[i] = None
            if IL.loc[i]["Farmers Market?"] == True:
                category[i] = "Farmer's Market"
            else: 
                category[i] = "Unknown"
            types[i] = None

            continue
    
        
        #check if response from Google closely matches retailer 
        add1 = address.split()[0]
        add2 = json["results"][0]["vicinity"].split()[0]

        #compare ignoring capitalization and ignoring unnecessary identifying #s from USDA entry
        name = name.lower()
        name = re.sub("\s\d*\w?$", "", name)
        jaro[i] = jellyfish.jaro_distance(name, json["results"][0]["name"].lower())

        if add1.lower() != add2.lower():
            check[i] = "Address mismatch"
            if jaro[i] < 0.6:
                check[i] = "Bad Match"
                ids[i]=None
                names[i]=None
                lats[i]=None
                lngs[i]=None
                adds[i]= None
                form_adds[i] = None
                phone[i] = None
                hours[i] = None
                website[i] = None
                url[i] = None
                rating[i] = None
                costs[i] = None
                price_level[i] = None
                yelp_prices[i] = None
                if IL.loc[i]["Farmers Market?"] == True:
                    category[i] = "Farmer's Market"
                else: 
                    category[i] = "Unknown"
                types[i] = None

                continue


        #add Google info to intermediary lists 
        ids[i] = json["results"][0]["place_id"]
        names[i] = json["results"][0]["name"]
        lats[i] = json["results"][0]["geometry"]["location"]["lat"]
        lngs[i] = json["results"][0]["geometry"]["location"]["lng"]
        adds[i] = json["results"][0]["vicinity"]
        if IL.loc[i]["Farmers Market?"] == True:
            category[i] = "Farmer's Market"
        else: 
            category[i] = categorize(json)
        types[i] = json["results"][0]["types"]

        if "price_level" in json["results"][0]:
            costs[i] = json["results"][0]["price_level"]
        else:
            costs[i] = None      

        #use placed ID to add Place Details Info to lists
        add_d, phone_d, hours_d, website_d, url_d, rating_d, price_d = get_details_info(json["results"][0]["place_id"],\
         key, KEY_INDEX, developerKeys)
        form_adds[i] = add_d
        phone[i] = phone_d
        hours[i] = hours_d
        website[i] = website_d
        url[i] = url_d
        rating[i] = rating_d
        price_level[i] = price_d

        #use phone number from google to get Yelp price
        if phone_d != None:
            yelp_price = get_yelp_price(phone_d, headers, url = 'https://api.yelp.com/v3/businesses/search/phone')
            yelp_prices[i] = yelp_price
        else:
            yelp_prices[i] = None
        
        #completed += 1
        #print (completed)

    #Add collected info to dataframe
    IL["place_id"] = ids
    IL["googlename"] = names
    IL["googlelat"] = lats
    IL["googlelon"] = lngs
    IL["googleaddress"] = adds
    IL['check'] = check
    IL["official_address"] = form_adds
    IL["phone number"] = phone
    IL["hours"] = hours
    IL["website"] = website
    IL["url"] = url
    IL["rating"] = rating
    IL["nearby_price"] = costs
    IL["details_price"] = price_level
    IL["Yelp_price"] = yelp_prices
    IL["category"] = category
    IL["type"] = types
    IL['multiple'] = multiple
    IL['how'] = how
    IL["jaro"] = jaro
    

    IL.to_csv(filename)



#Below are the helper functions used within get_info!
@backoff.on_exception(backoff.expo, requests.exceptions.ConnectionError, max_tries=3)
def get_place_url(lat, lon, keyword, radius, key):
    """
    Performs Google Nearby Search Request based on parameters and returns json of responses. 
    """
    
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location\
={},{}&keyword={}&radius={}&key={}".format(lat, lon, keyword, radius, key)
    #print (url)
    r = requests.get(url)
    return r.json()

def get_place_details_url(placeid, key):
    """
    Performs Google Place Details request and returns json of response. 
    """
    
    url = "https://maps.googleapis.com/maps/api/place/details/json?\
placeid={}&key={}".format(placeid, key)
    #print (url)
    r = requests.get(url)
    return r.json()

def get_yelp_keys():
    """
    Returns header required to use Yelp API. 
    """
    
    app_id = "uc-LC0hKhl1jNEwzmyafRQ"
    app_secret = "cCisYBB8tDDnVD2qn7MNdUx3mv5McEggAkvWcIHoG7WiJbVtDgl4qnqYLNM3P7Sg"

    data = {'grant_type': 'client_credentials', "client_id": app_id, "client_secret": app_secret}

    token = requests.post('https://api.yelp.com/oauth2/token', data=data)
    access_token = token.json()['access_token']
    headers = {'Authorization': 'bearer %s' % access_token}
    return headers

def get_yelp_price(phone, headers, url = 'https://api.yelp.com/v3/businesses/search/phone'):
    """
    Given retailer phone number, performs Yelp Phone Search and return retailer price.
    """

    for character in string.punctuation + " ":
        phone = phone.replace(character, "")
    format_phone = "+1" + phone
    param = {'phone': format_phone}
    resp = requests.get(url=url, params=param, headers=headers)

    if resp.json()['businesses'] == []:
        return None
    elif "price" not in resp.json()["businesses"][0]:
        return None
    return resp.json()['businesses'][0]['price']

def get_details_info(place_id, key, KEY_INDEX, developerKeys):
    """
    Use developer key to perform Place Details Search on the matched Place ID \
    from the Nearby search. When info is available, returns formatted address, \
    phone number, hours, website, url, rating, price for given Place ID. 

    """
    json = get_place_details_url(place_id, key)
    #if reached requests limit for key, find next valid key in the list. 
    while json["status"] == "OVER_QUERY_LIMIT":
        KEY_INDEX += 1
        key = developerKeys[KEY_INDEX]
        json = get_place_details_url(place_id, key)
            
    form_add = json["result"]["formatted_address"]
    url = json["result"]["url"]
    if "formatted_phone_number" in json["result"]:
        phone = json["result"]["formatted_phone_number"]
    else:
        phone = None
    if "opening_hours" in json["result"]:
        hours = json["result"]["opening_hours"]["weekday_text"]
    else: 
        hours = None
    if "website" in json["result"]:
        website = json["result"]["website"]
    else:
        website = None
    if "rating" in json["result"]:
        rating = json["result"]["rating"]
    else:
        rating = None
    if "price_level" in json["result"]:
        price = json["result"]["price_level"]
    else:
        price = None
    return form_add, phone, hours, website, url, rating, price
    
def categorize(json):
    """
    Given information in json returned from Google Places Nearby Search, \
    returns appropriate category for retailer. 
    """
    types_list = json["results"][0]["types"]

    if "gas_station" in types_list: 
        category = "Gas Station"
    elif "convenience_store" in types_list or "liquor_store" in types_list:
        category = "Convenience Store"
    elif "grocery_or_supermarket" in types_list and "convenience_store" not in types_list:
        category = "Grocery"
    elif "bakery" in types_list or "cafe" in types_list:
        category = "Other"
    else:
        category = "Other"

    return category

def best_result(json, name):
    """
    Compares name of entry in USDA database to json, which includes all results \
    returned by nearby search. Returns the entry in json that best matches given name. 
    """
    best = 0
    best_dist = 0
    for i in range(len(json["results"])):
        result = json["results"][i]["name"]
        g_name = name.lower()
        g_name = re.sub("\s\d*\w?$", "", g_name)
        if jellyfish.jaro_distance(result.lower(), g_name) > best_dist:
            best = i
            best_dist = jellyfish.jaro_distance(result.lower(), g_name)
    json = json["results"][best]

    return json





#################################################################


#This is code that may be used in the future for record linkage. 
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
