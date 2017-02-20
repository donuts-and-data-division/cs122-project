from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class SnapLocations(models.Model):
    googlename = models.CharField(max_length=100)
    point = models.PointField(srid = 4312, default = (0,0))
    googleaddress = models.CharField(max_length = 200)

    # Returns the string representation of the model.
    def __str__(self):              
        return self.googlename
