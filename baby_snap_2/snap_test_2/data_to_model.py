'''
Reads data from csv to models.SnapLocations

Inputs: csv_file with columns that match models.SnapLocations
'''

from snap_test_2.models import SnapLocations
from django.contrib.gis.geos import Point
import csv


csv_file = 'snapresultstestChicago1.csv'
DOLLAR_SIGNS = {'0': 0, '$': 1, '$$': 2, '$$$': 3, '$$$$': 4, '$$$$$': 5}

with open(csv_file) as f:
    ls = list(csv.reader(f))
    headers = ls[0]
    for ind, line in enumerate(ls[1:]):
        double_value = line[headers.index('Double Value')]
        farmers_mkt = line[headers.index('Farmers Market?')]
        if line[headers.index('place_id')]:
            # found record linkage to google; use google places information
            # 94% of Chicago retailers fall into this category
            name = line[headers.index('googlename')]
            address = line[headers.index('official_address')]
            place_id = line[headers.index('place_id')]
            geom = Point(float(line[headers.index('googlelon')]), float(line[headers.index('googlelat')]))
            phone = line[headers.index('phone number')]
            website = line[headers.index('website')]
            store_category = line[headers.index('category')]
            
            rating = line[headers.index('rating')]
            if rating == '':
                rating = 0.0

            hours_list = line[headers.index('hours')]
            if hours_list != '':
                hours = hours_list.replace(',', '\n')
            else:
                hours = ''

            yelp_price = line[headers.index('Yelp_price')]
            if yelp_price == 0 or yelp_price == '':
                # no yelp price levels; use Google's instead
                price_level = line[headers.index('details_price')]
                
            else:
                # convert yelp dollar signs to numbers
                price_level = DOLLAR_SIGNS[yelp_price]
            if price_level == '':
                price_level = 0
            price_level = int(float(price_level))
        else:
            # no reliable record linkage to google; use original information
            # 6% of Chicago retailers fall into this category
            name = line[headers.index('Store_Name')]
            street = line[headers.index('Address')]
            street2 = line[headers.index('Address Line #2')]
            city = line[headers.index('City')]
            state = line[headers.index('State')]
            zipcode = line[headers.index('Zip5')]
            address = street + ' '+ street2 + ', ' + city + ', ' + state + ' ' + zipcode + ', ' + 'USA'
            geom = Point(float(line[headers.index('Longitude')]), float(line[headers.index('Latitude')]))
            place_id = ''
            phone = ''
            website = ''
            rating = 0.0
            store_category = ''
            hours = ''
            price_level = 0
        
        try:
            SnapLocations(  
                double_value = double_value,
                farmers_mkt = farmers_mkt,
                name = name,
                address = address,
                geom = geom,
                place_id = place_id,
                phone= phone,
                website = website,
                rating = rating,
                store_category = store_category,
                hours = hours,
                price_level = price_level
            ).save()
        except:
            print("Trouble in row {}".format(ind), price_level)
