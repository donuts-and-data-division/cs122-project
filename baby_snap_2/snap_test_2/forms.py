from django import forms
from .models import FoodPrices
#Inspired by ui in pa3
def types_list(lst):
    return [(x,x) for x in lst]
    


class SearchForm(forms.Form):
    location = forms.CharField(widget = forms.TextInput(), label='Near', max_length=100)
    
    types = [('Grocery', 'Grocery'), 
        ('Convenience Store', "Convenience Store"),
        ('Farmers Market', "Farmer's Market"), 
        ('Gas Station', "Gas Station")]
    retailer_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=types, label='Retailer Type', required = False)
    
    dollar_signs = [('$', '$'), ('$$','$$'), ('$$$','$$$')]
    price = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=dollar_signs, label='Price', required = False)
    
    distances = [('1 mile', '1 mile'), ('5 miles', '5 miles'), ('10 miles', '10 miles')]
    radius = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=distances, label='Radius', required = False)
    
    stars = [('1 star', '1 star'),('2 stars', '2 stars'),('3 stars', '3 stars'), ('4 stars', '4 stars'), ('5 stars', '5 stars')]
    rating = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=stars, label='Average Rating', required = False)
    
    sw_lat = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'sw_lat'}))
    sw_lon = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'sw_lon'}))
    ne_lat = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'ne_lat'}))
    ne_lon = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'ne_lon'}))
   # Need to remove bullet points from check boxes with CSS

class FilterForm(forms.Form):
    types = types_list(['Grocery', "Farmer's Market", 'Convenience Store', 'Gas Station'])
    retailer_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=types, label='Retailer Type', required = False)
    
    dollar_signs = types_list(["$","$$","$$$"])
    price = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=dollar_signs, label='Price', required = False)
     
    stars = [('1 star', '1 star'),('2 stars', '2 stars'),('3 stars', '3 stars'), ('4 stars', '4 stars'), ('5 stars', '5 stars')]
    rating = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=stars, label='Average Rating', required = False)


class PricesForm(forms.Form):
    name = forms.CharField( widget=forms.HiddenInput(attrs={'id':'name'}))
    retailer_type = forms.CharField( widget=forms.HiddenInput(attrs={'id':'retailer_type'}))
    price = forms.CharField( widget=forms.HiddenInput(attrs={'id':'price'}))
    place_id = forms.CharField( widget=forms.HiddenInput(attrs={'id':'place_id'}))


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

    food = forms.ModelChoiceField(queryset=FoodPrices.objects.all(), empty_label = "Build your list", label="")
    #quantity = forms.CharField(max_length=3, 
        #widget=forms.Select(choices=QUANTITY_CHOICES))

    class Meta:
        model = FoodPrices
        exclude = ['food_name', 'food_quantity', 'food_price', 'date_last_updated', 'food_type']

    