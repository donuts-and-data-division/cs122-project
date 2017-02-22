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
    for line in ls[1:]:
        googlename = line[1]
        geom = Point(float(line[3]), float(line[2]))
        googleaddress = line[4]
        try:
            SnapLocations(googlename = googlename, geom = geom, googleaddress = googleaddress).save()
        except:
            print("Trouble in row {}".format(i))
