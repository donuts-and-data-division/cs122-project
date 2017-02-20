from django.db import models
from django.contrib.gis.db import models as gismodels

# Create your models here.
class SnapLocations(gismodels.Model):
    googlename = models.CharField(max_length=100)
    point = gismodels.PointField()
    googleaddress = models.CharField(max_length = 200)
    

    # Returns the string representation of the model.
    def __str__(self):              
        return self.googlename