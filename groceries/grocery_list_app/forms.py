from django import forms
from .models import FoodPrices

QUANTITY_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
)

class GroceryForm(forms.ModelForm):

    food = forms.ModelChoiceField(queryset=FoodPrices.objects.all(), 
        empty_label="Select a food item")

    quantity = forms.CharField(max_length=3, 
        widget=forms.Select(choices=QUANTITY_CHOICES))

    class Meta:
        model = FoodPrices
        exclude = ['food_name', 'food_quantity', 'food_price', 'date_last_updated']

