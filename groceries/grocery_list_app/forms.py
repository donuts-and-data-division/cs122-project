from django import forms
from .models import FoodPrices

QUANTITY_CHOICES = (
    (0.25, 0.25),
    (0.5, 0.5),
    (0.75, 0.75),
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

    #instead of .all we need to filter by store type to adjust the dropdown menu
    #store type will come from the view maybe ?

    food = forms.ModelChoiceField(queryset=FoodPrices.objects.all())

    quantity = forms.CharField(max_length=3, 
        widget=forms.Select(choices=QUANTITY_CHOICES))

    class Meta:
        model = FoodPrices
        exclude = ['food_name', 'food_quantity', 'food_price', 'date_last_updated']

