from django.db import models
from django.contrib.gis.db import models as gismodels
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User


# Create your models here.
class SnapLocations(models.Model):
    double_value = models.BooleanField()
    farmers_mkt = models.BooleanField()
    name = models.CharField(max_length = 5000)
    address = models.CharField(max_length = 5000)
    place_id = models.CharField(max_length = 5000)
    geom = gismodels.PointField()
    phone = models.CharField(max_length = 5000)
    hours = models.CharField(max_length = 5000)
    website = models.CharField(max_length = 5000)
    rating = models.FloatField() # NOTE: rating = 0 means not available from Google
    store_category = models.CharField(max_length = 5000)
    price_level = models.IntegerField()

    # Returns the string representation of the model.
    def __str__(self):              
        return self.googlename


class FoodPrices(models.Model):
    food_name = models.CharField(max_length=100)
    food_quantity = models.CharField(max_length=20)
    food_price = models.FloatField()
    date_last_updated = models.DateTimeField(default=timezone.now)
    food_type = models.CharField(max_length=50, default=0)


    
    # Returns the string representation of the model.
    def __str__(self):              
        return self.food_name


class UserPriceDataModel(models.Model):
    store_id = models.IntegerField()
    food_id = models.IntegerField()
    user_input = models.FloatField()
    # Store Regression Estimates:
    for store_type in range(6):
        for price_level in range(6):
            exec("s{}_p{} = models.IntegerField()".format(store_type, price_level))
          
class StorePriceModel(models.Model):
    store_id = models.IntegerField()
    food_id = models.IntegerField()



    
