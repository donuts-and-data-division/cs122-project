from django import forms
from .models import FoodPrices

class GroceryForm(forms.ModelForm):

    class Meta:
        model = FoodPrices
        fields = ('food_name', 'food_quantity',)