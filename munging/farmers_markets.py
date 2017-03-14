import bs4
import urllib3
import csv
import re
import pandas as pd
import requests


def get_markets(filename):
    """
    From DHS website, create dataframe with Farmer's Markets name, latitude/longitude
    address, phone number, and whether market accepts double value coupons. 
    """

    pm = urllib3.PoolManager()
    html = pm.urlopen(url="http://www.dhs.state.il.us/page.aspx?item=44172", method="GET").data
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
            city = re.findall('\\n(.*)\,\s+[A-Z]{2}', market.text)[0]
            state = re.findall('\\n.*\,\s+([A-Z]{2})', market.text)[0]

            if len(re.findall("Double Value Coupons", market.text)) == 1:
                double_value = True

            if len(re.findall("[A-Z]{2}\s+(\d{5})", market.text)) > 0:
                zipcode = re.findall("[A-Z]{2}\s+(\d{5})", market.text)[0]

            if len(re.findall("\(\d{3}\)\s\d{3}-\d{4}", market.text)) > 0:
                phone = re.findall("\(\d{3}\)\s?\d{3}-\d{4}", market.text)[0]

            market_list.append([market_name, address, city, state, zipcode, phone, double_value])

    df = pd.DataFrame(market_list)
    
    #manual edits
    df.loc[12, 1] = "825 18th St."
    df.loc[13, 1] = "6100 S. Blackstone Ave."
    df.loc[13, 0] = "Experimental Station"
    df.loc[15, 1] = "W. Lake St. & N. Central Ave."
    df.loc[20, 1] = "W. Harrison St. & S. Central Ave."
    df.loc[56, 1] = "79th & South Shore Drive (corner)"
    df.loc[56, 2] = "Chicago"
    df.loc[70, 1] = "University Place & Oak Avenue"
    df.loc[75, 2] = "Benton"
    df.loc[81, 1] = "11141 County Rd 300 E"
    df.loc[83, 1] = "Corner of Cherry Lane & Meadow Rd."

    #adding lat/lon
    lat_list = []
    lon_list = []

    for row in df.values:
        address = row[1]
        city = row[2]
        state = row[3]

        url = get_url(address, city, state)
        lat, lon = get_lat_lon(url)

        lat_list.append(lat)
        lon_list.append(lon)

    lat_df = pd.DataFrame(lat_list)
    lon_df = pd.DataFrame(lon_list)

    final_df = pd.concat([df, lat_df, lon_df], axis = 1)
    final_df.columns = ['Market Name', 'Address', 'City', 'State', 'Zipcode', 'Phone', 'Double Value', 'Latitude', 'Longitude']

    final_df.to_csv(path_or_buf = filename)
    #number of markets should be 102


def get_url(address, city, state):
    """
    Returns URL for google search. 
    """

    query_lst = address.split() + city.split() + state.split()
    query = "+".join(query_lst)
    key = "AIzaSyDQsfHu5QVO-s3Xttn_twLLr6E3ggsIZDk"

    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(query, key)

    return url


def get_lat_lon(url):
    """
    Returns latitude and longitude from Google API response. 
    """
    r = requests.get(url)
    json = r.json()

    if json['results'] == []:
        return (None, None)

    lat = json["results"][0]["geometry"]["location"]["lat"]
    lon = json["results"][0]["geometry"]["location"]["lng"]

    return (lat, lon)