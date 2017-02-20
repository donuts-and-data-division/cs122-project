from snap_test_2.models import SnapLocations
import pandas as pd
from django.contrib.gis.geos import Point

def data_to_model(csv_file):
    f = pd.read_csv(csv_file)
    for i in range(len(f)):
        snap_spot= SnapLocations(googlename = f.loc[i][1], 
                                #lon, lat
                                point = Point(f.loc[i][3], f.loc[i][2]),
                                googleaddress = f.loc[i][4],)

        try:
            snap_spot.save()
        except:
            print("Trouble in row {}".format(i))


