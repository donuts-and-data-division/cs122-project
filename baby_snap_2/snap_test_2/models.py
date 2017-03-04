from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User


# Create your models here.
class SnapLocations(models.Model):
    googlename = models.CharField(max_length=100)
    geom = gismodels.PointField()
    googleaddress = models.CharField(max_length = 200)
    place_id = models.CharField(max_length = 100)

    # Returns the string representation of the model.
    def __str__(self):              
        return self.googlename


class FoodPrices(models.Model):
    food_name = models.CharField(max_length=100)
    food_quantity = models.CharField(max_length=20)
    food_price = models.FloatField()
    date_last_updated = models.DateTimeField(default=timezone.now)

    # Returns the string representation of the model.
    def __str__(self):              
        return self.food_name