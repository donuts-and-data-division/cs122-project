'''
Reads data from csv to models.SnapLocations

Inputs: csv_file with columns that match models.SnapLocations
'''

from snap_test_2.models import SnapLocations
from django.contrib.gis.geos import Point
import csv


csv_file = 'practice_with_pid.csv'

with open(csv_file) as f:
    ls = list(csv.reader(f))
    # UPDATE THESE
    name_index = ls[0].index('googlename')
    lat_index = ls[0].index('googlelat')
    lon_index = ls[0].index('googlelon')
    googleaddress_index = ls[0].index('googleaddress')
    place_id_index = ls[0].index('place_id')
    print(lat_index, lon_index)

    for line in ls[1:]:
        print("ok",line)
        if line[place_id_index]:
            googlename = line[name_index]
            geom = Point(float(line[lon_index]), float(line[lat_index]))
            googleaddress = line[googleaddress_index]
            place_id = line[place_id_index]
            try:
                SnapLocations(googlename = googlename, geom = geom, 
                    googleaddress = googleaddress, place_id = place_id).save()
            except:
                print("Trouble in row {}".format(i))

