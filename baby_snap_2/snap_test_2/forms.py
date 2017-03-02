from django import forms
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
   # Need to remove bullet points from check boxes with CSS'''

    types = types_list(['Grocery', "Farmer's Market", 'Convenience Store', 'Gas Station'])
    retailer_type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=types, label='Retailer Type', required = False)
    
    dollar_signs = types_list(["$","$$","$$$"])
    price = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=dollar_signs, label='Price', required = False)
     
    stars = [('1 star', '1 star'),('2 stars', '2 stars'),('3 stars', '3 stars'), ('4 stars', '4 stars'), ('5 stars', '5 stars')]
    rating = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=stars, label='Average Rating', required = False)


class GroceriesForm(forms.Form):
    name = forms.CharField( widget=forms.HiddenInput(attrs={'id':'name'}))
    retailer_type = forms.CharField( widget=forms.HiddenInput(attrs={'id':'retailer_type'}))
    price = forms.CharField( widget=forms.HiddenInput(attrs={'id':'price'}))

class PricesForm(forms.Form):
    name = forms.CharField( widget=forms.HiddenInput(attrs={'id':'name'}))
    retailer_type = forms.CharField( widget=forms.HiddenInput(attrs={'id':'retailer_type'}))
    price = forms.CharField( widget=forms.HiddenInput(attrs={'id':'price'}))
    place_id = forms.CharField( widget=forms.HiddenInput(attrs={'id':'place_id'}))

    