from django.shortcuts import render
from .forms import GroceryForm
from django.http import JsonResponse
# Create your views here.
#def grocery_list(request):
#    return render(request, 'grocery_list_app/grocery_list.html', {})

from .models import FoodPrices

def submit_grocery_list(request):
    
    if request.method == "POST":
        form = GroceryForm(request.POST)     

    else:
        form = GroceryForm()

    #this view will actually be coming from the map part, and will redirect to the grocery list page
    #make a dictionary with dollar sign info and list of foods available at that type of store?
    #add that dictionary to the render thing
    #somehow edit the dropdown menu on the form based on the list of foods...

    return render(request, 'grocery_list_app/grocery_list_2.html', {'form': form})


def cash_register(request):
    food_id = request.GET.get('food_id', None)
    data = {
            'food_price': FoodPrices.objects.get(id=food_id).food_price,
            'food_quantity': FoodPrices.objects.get(id=food_id).food_quantity,
            'food_name': FoodPrices.objects.get(id=food_id).food_name
            }

    #probably add dollar signs to this dictionary
    #e.g. 'dollar_sign': 1

    return JsonResponse(data)
