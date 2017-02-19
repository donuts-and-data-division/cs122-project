from django.db import models

# Create your models here.
class SnapLocations(models.Model):
    googlename = models.CharField(max_length=100)
    point = models.PointField(sid = 4312)
    googleaddress = models.CharField(max_length = 200)

    # Returns the string representation of the model.
    def __str__(self):              
        return self.googlename
