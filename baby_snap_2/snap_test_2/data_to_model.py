'''
Reads data from csv to models.SnapLocations

Inputs: csv_file with columns that match models.SnapLocations
'''

from snap_test_2.models import SnapLocations
from django.contrib.gis.geos import Point
import csv


csv_file = 'snapresultstestChicago1.csv'
#DOLLAR_SIGNS = {'0': 0, '$': 1, '$$': 2, '$$$': 3, '$$$$': 4, '$$$$$': 5}

with open(csv_file) as f:
    ls = list(csv.reader(f))
    headers = ls[0]
    for ind, line in enumerate(ls[1:]):
        store_id = line[0]
        if line[headers.index('place_id')]:
            # found record linkage to google; use google places information
            # 94% of Chicago retailers fall into this category
            store_name = line[headers.index('googlename')]
            address = line[headers.index('official_address')]
            place_id = line[headers.index('place_id')]
            geom = Point(float(line[headers.index('googlelon')]), float(line[headers.index('googlelat')]))
            phone = line[headers.index('phone number')]
            if phone == '':
                phone = 'Not available'

            website = line[headers.index('website')]
            if website == '':
                website = 'Not available'
            store_category = line[headers.index('category')]
            
            rating = line[headers.index('rating')]
            if rating == '':
                rating = 'Not available'

            hours_list = line[headers.index('hours')]
            if hours_list != '':
                hours = hours_list.replace(',', '\n')
                hours = hours_list.replace(']', '')
                hours = hours_list.replace('[', '')
            else:
                hours = 'Not available'

            yelp_price = line[headers.index('Yelp_price')]
            if yelp_price == '0' or yelp_price == '':
                # no yelp price levels; use Google's instead
                price_level = line[headers.index('details_price')]
            else:
                # convert yelp dollar signs to numbers
                price_level = yelp_price
            if price_level == '':
                price_level = 'Not available'
            
        else:
            # no reliable record linkage to google; use original information
            # 6% of Chicago retailers fall into this category
            store_name = line[headers.index('Store_Name')]
            street = line[headers.index('Address')]
            street2 = line[headers.index('Address Line #2')]
            city = line[headers.index('City')]
            state = line[headers.index('State')]
            zipcode = line[headers.index('Zip5')]
            address = street + ' '+ street2 + ', ' + city + ', ' + state + ' ' + zipcode + ', ' + 'USA'
            geom = Point(float(line[headers.index('Longitude')]), float(line[headers.index('Latitude')]))
            place_id = 'Not available'
            phone = 'Not available'
            website = 'Not available'
            rating = 'Not available'
            store_category = 'Not available'
            hours = 'Not available'
            price_level = 'Not available'
        
        farmers_mkt = line[headers.index('Farmers Market?')]
        if farmers_mkt == True: 
            if line[headers.index('Double Value')] == True:
                double_value = 'Yes'
            else:
                double_value = 'No'
        else:
            double_value = "N/A"
        
        try:
            SnapLocations(  
                store_id = store_id,
                double_value = double_value,
                farmers_mkt = farmers_mkt,
                store_name = store_name,
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
            print("Trouble in row {}".format(ind), farmers_mkt, store_name)