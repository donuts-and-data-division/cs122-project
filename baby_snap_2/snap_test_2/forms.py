from django import forms
from .models import FoodPrices
#Inspired by ui in pa3
def types_list(lst):
    return [(x,x) for x in lst]
    

'''
class SearchForm(forms.Form):
    location = forms.CharField(widget = forms.TextInput(), label='Near', max_length=100)
    
    types = [('Grocery', 'Grocery'), 
        ('Convenience Store', "Convenience Store"),
        ('Farmers Market', "Farmer's Market"), 
        ('Gas Station', "Gas Station"),
        ('Other', "Other")]
    retailer_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=types, label='Retailer Type', required = False)
    
    dollar_signs = [(1, '$'), (2, '$$'), (3,'$$$'), (4,'$$$$'), (5, '$$$$$')]
    price = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=dollar_signs, label='Price', required = False)
    
    # could we make these actual stars?
    stars = [('1 star', '1 star'),('2 stars', '2 stars'),('3 stars', '3 stars'), ('4 stars', '4 stars'), ('5 stars', '5 stars')]
    rating = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=stars, label='Average Rating', required = False)
    
    sw_lat = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'sw_lat'}))
    sw_lon = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'sw_lon'}))
    ne_lat = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'ne_lat'}))
    ne_lon = forms.FloatField( widget=forms.HiddenInput(attrs={'id':'ne_lon'}))
   # Need to remove bullet points from check boxes with CSS
'''
class FilterForm(forms.Form):
    types = types_list(['Grocery',"Farmer's Market", 'Convenience Store', 'Gas Station', 'Other'])
    retailer_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=types, label='Retailer Type', required = False)
    
    dollar_signs = types_list(["$","$$","$$$", "$$$$", "$$$$$"])
    price = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=dollar_signs, label='Price', required = False)
     
    stars = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    rating = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=stars, label='Average Rating', required = False)


class PricesForm(forms.Form):
    name = forms.CharField( widget=forms.HiddenInput(attrs={'id':'name'}))
    retailer_type = forms.CharField( widget=forms.HiddenInput(attrs={'id':'retailer_type'}))
    price = forms.CharField( widget=forms.HiddenInput(attrs={'id':'price'}))
    place_id = forms.CharField( widget=forms.HiddenInput(attrs={'id':'place_id'}))


class GroceryForm(forms.ModelForm):
    
    fruits_and_veggies = forms.ModelChoiceField(queryset=FoodPrices.objects.filter(food_type="Fruits & Vegetables").order_by('food_name'), \
        empty_label = "Fruits & Vegetables", label="", required=False)

    meat_and_fish = forms.ModelChoiceField(queryset=FoodPrices.objects.filter(food_type="Meat & Fish").order_by('food_name'), \
        empty_label = "Meat & Fish", label="", required=False)
    
    dairy = forms.ModelChoiceField(queryset=FoodPrices.objects.filter(food_type="Dairy").order_by('food_name'), \
        empty_label = "Dairy", label="", required=False)

    grains = forms.ModelChoiceField(queryset=FoodPrices.objects.filter(food_type="Grains").order_by('food_name'), \
        empty_label = "Grains", label="", required=False)

    other = forms.ModelChoiceField(queryset=FoodPrices.objects.filter(food_type="Other").order_by('food_name'), \
        empty_label = "Other", label="", required=False)
    
    class Meta:
        model = FoodPrices
        exclude = ['food_name', 'food_quantity', 'food_price', 'date_last_updated', 'food_type']

    