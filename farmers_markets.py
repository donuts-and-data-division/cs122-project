import bs4
import urllib3
import csv
import re
import pandas as pd


def get_markets(url, filename):

    pm = urllib3.PoolManager()
    html = pm.urlopen(url=url, method="GET").data
    soup = bs4.BeautifulSoup(html, "lxml")

    tags = soup.find_all("ul", class_ = ["discBullets", "discbullets", "disBullets"])

    market_list = []

    for tag in tags[:42]:
        markets = tag.find_all("li")

        for market in markets:

            zipcode = None
            phone = None
            double_value = False
            market.text.replace('\xa0', ' ')

            market_tag = market.find_all("strong")
            market_name = market_tag[0].text
            address = re.findall("\d+.+?(?=\r)", market.text)[0]
            city_state = re.findall('\\n(.*\,\s+[A-Z]{2})', market.text)[0]

            if len(re.findall("Double Value Coupons", market.text)) == 1:
                double_value = True

            if len(re.findall("[A-Z]{2}\s+(\d{5})", market.text)) > 0:
                zipcode = re.findall("[A-Z]{2}\s+(\d{5})", market.text)[0]

            if len(re.findall("\(\d{3}\)\s\d{3}-\d{4}", market.text)) > 0:
                phone = re.findall("\(\d{3}\)\s?\d{3}-\d{4}", market.text)[0]

            market_list.append([market_name, address, city_state, zipcode, phone, double_value])

    #number of markets should be 102

    final_list = []
    header = ['market name', 'address', 'city/state', 'zipcode', 'phone', 'double value']
    final_list.append(header)

    for row in market_list:
        final_list.append(row)

    f = open(filename, 'wt')
    writer = csv.writer(f)
    for row in final_list:
        writer.writerow(row)

    f.close()

    return f


def get_url(name, city_state, key):

    c_s = city_state.replace(',', '')
    query_lst =  name.split() + c_s.split()
    query = "+".join(query_lst)

    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query={}&key={}".format(query, key)

    return url


'''
def get_place_id():
    IL_filename = "IL-100.csv"
    IL = pd.read_csv(IL_filename)

    developerKeys = ["AIzaSyCGt79JrG0sym4cyrs6YabCyy76zpnB828",\
    "AIzaSyBUDrUeEyJyUNwQl1oVJCydSFPb5fCMQvw", "AIzaSyC9dbLTJ-aU2VL0r1Zhpzlxx99TrW-tpMM",\
    "AIzaSyBkWTxpnmygafi2mFETLRumyw0OlY_ftwM"]
    
    key = developerKeys[3]

    ids = []

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

    '''