from django import forms

class SearchNearby(forms.Form):
    search_nearby = forms.CharField(label = "Enter address", max_length = 500)