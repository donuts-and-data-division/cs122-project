from django.db import models
#from django.contrib.gis.db import models as gismodels
from djgeojson.fields import PointField

# Create your models here.
class SnapLocations(models.Model):
    googlename = models.CharField(max_length=100)
    geom = PointField()
    googleaddress = models.CharField(max_length = 200)
    

    # Returns the string representation of the model.
    def __str__(self):              
        return self.googlename