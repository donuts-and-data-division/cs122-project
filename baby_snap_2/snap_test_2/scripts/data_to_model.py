'''
Reads data from csv to models.SnapLocations

Inputs: csv_file
'''

from snap_test_2.models import SnapLocations
from django.contrib.gis.geos import Point
import csv

SnapLocations.objects.all().delete()
csv_file = 'snapresultstestChicago2.csv'
DOLLAR_SIGNS = {'': 'Not available', '1.0': '$', '2.0': '$$', '3.0': '$$$', '4.0': '$$$$', '5.0': '$$$$$'}

with open(csv_file) as f:
    ls = list(csv.reader(f))
    headers = ls[0]
    # manual deduping unique locations in original data source that matched to duplicate place ids
    duplicates = [1508, 1306, 139, 167, 738, 1434, 125, 540, 1214, 1250, 1367, 1503, 306, 518, 835, 522, 982,
    284, 393, 588, 274, 1745, 287, 1432, 1076, 1138, 189, 931, 1910, 316, 512, 1189, 490, 1338, 895, 332, 586, 2034]
    for ind, line in enumerate(ls[1:]):
        store_id = line[0]
        if line[headers.index('place_id')] and store_id not in duplicates:
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
                rating = 0

            hours_list = line[headers.index('hours')]
            if hours_list != '':
                hours = hours_list.replace(']', '').replace('[', '').replace("'", "")
            else:
                hours = 'Not available'

            yelp_price = line[headers.index('Yelp_price')]
            if yelp_price == '0' or yelp_price == '':
                # no yelp price levels; use Google's instead
                price_level = line[headers.index('details_price')]
                price_level = DOLLAR_SIGNS[price_level]
            else:
                # use yelp price
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
            rating = 0
            store_category = 'Not available'
            hours = 'Not available'
            price_level = 'Not available'
        
        farmers_mkt = line[headers.index('Farmers Market?')]
        if farmers_mkt == 'True': 
            if line[headers.index('Double Value')] == 'True':
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

# manually deduping obvious duplicates in original data source 
to_remove = [1331, 2179, 2182, 724, 2029]
SnapLocations.objects.filter(store_id__in = to_remove).delete()