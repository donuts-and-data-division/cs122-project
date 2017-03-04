from django.db import models
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import User

class FoodPrices(models.Model):
    food_name = models.CharField(max_length=100)
    food_quantity = models.CharField(max_length=20)
    food_price = models.FloatField()
    date_last_updated = models.DateTimeField(default=timezone.now)
    food_type = models.CharField(max_length=50)

    # Returns the string representation of the model.
    def __str__(self):              
        return self.food_name


#class StorePrices(models.Model):
    #store_name = model.CharField(max_length = 100)
    #price = model.FloatField()

    #def __str__(self):
        #return self.price