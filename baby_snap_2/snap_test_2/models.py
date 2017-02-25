from django.db import models
#from django.contrib.gis.db import models as gismodels
from django.contrib.gis.db import models as gismodels

# Create your models here.
class SnapLocations(models.Model):
    googlename = models.CharField(max_length=100)
    geom = gismodels.PointField()
    googleaddress = models.CharField(max_length = 200)
    #place_id = models.CharField(max_length = 100)

    # Returns the string representation of the model.
    def __str__(self):              
        return self.googlename