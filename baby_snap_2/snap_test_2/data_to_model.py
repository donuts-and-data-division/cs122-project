'''
Reads data from csv to models.SnapLocations

Inputs: csv_file with columns that match models.SnapLocations
'''

from snap_test_2.models import SnapLocations
from django.contrib.gis.geos import Point
import csv


csv_file = 'practice.csv'

with open(csv_file) as f:
    ls = list(csv.reader(f))
    # UPDATE THESE
    name_index = ls[0].index('googlename')
    lat_index = ls[0].index('googlename')
    lon_index = ls[0].index('googlename')
    place_id_index = ls[0].index('googlename')

    for line in ls[1:]:
        googlename = line[1]
        geom = Point(float(line[3]), float(line[2]))
        googleaddress = line[4]
        place_id = line[9]
        try:
            SnapLocations(googlename = googlename, geom = geom, 
                googleaddress = googleaddress, place_id = place_id).save()
        except:
            print("Trouble in row {}".format(i))

