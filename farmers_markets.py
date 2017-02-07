import bs4
import urllib3
import csv
import re


def get_markets(url, filename):

    pm = urllib3.PoolManager()
    html = pm.urlopen(url=url, method="GET").data
    soup = bs4.BeautifulSoup(html, "lxml")

    tags = soup.find_all("ul", class_ = ["discBullets", "discbullets", "disBullets"])

    market_list = []

    for tag in tags[:39]:
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
