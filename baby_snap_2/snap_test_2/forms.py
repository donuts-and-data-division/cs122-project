from django import forms
from .models import FoodPrices

#Inspired by ui in pa3
def types_list(lst):
    return [(x,x) for x in lst]
    
class FilterForm(forms.Form):
    types = types_list(['Grocery',"Farmer's Market", 'Convenience Store', 'Gas Station', 'Other'])
    retailer_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=types, label='Retailer Type', required = False)
    
    dollar_signs = types_list(["$","$$","$$$", "$$$$"])
    price = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=dollar_signs, label='Price', required = False)
     
    stars = [(0,""), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    rating = forms.ChoiceField(choices=stars, label='Average Rating', required = False)

    participating = types_list(['Participating locations'])
    double_value = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label = "Double Value Coupon Program (farmers markets only)", required=False, choices= participating)

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

    