import bs4
import urllib3
import csv
import re
import pandas as pd
import requests


def get_markets(filename):

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

            url = get_url(address, city, state)
            lat, lon = get_lat_lon(url)

            market_list.append([market_name, address, city, state, zipcode, phone, lat, lon, double_value])


    #number of markets should be 102

    final_list = []
    header = ['market name', 'address', 'city', 'state', 'zipcode', 'phone', 'latitude', 'longitude', 'double value']

    final_list.append(header)

    for row in market_list:
        final_list.append(row)

    f = open(filename, 'wt')
    writer = csv.writer(f)
    for row in final_list:
        writer.writerow(row)

    f.close()

    return f


def get_url(address, city, state):

    query_lst = address.split() + city.split() + state.split()
    query = "+".join(query_lst)
    key = "AIzaSyDQsfHu5QVO-s3Xttn_twLLr6E3ggsIZDk"

    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(query, key)

    return url


def get_lat_lon(url):
    r = requests.get(url)
    json = r.json()

    if json['results'] == []:
        return (None, None)

    lat = json["results"][0]["geometry"]["location"]["lat"]
    lon = json["results"][0]["geometry"]["location"]["lng"]

    return (lat, lon)