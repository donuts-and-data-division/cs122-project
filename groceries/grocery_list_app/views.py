from django.shortcuts import render
from .forms import GroceryForm
from .models import FoodPrices
from django.forms.models import model_to_dict

def submit_grocery_list(request):
    
    if request.method == "POST":
        form = GroceryForm(request.POST)
        

    else:
        form = GroceryForm()

    #food_list = FoodPrices.objects.all()

    qset = FoodPrices.objects.all()
    food_dict = {}

    for instance in qset:
        item_dict = model_to_dict(instance)
        food_dict[instance.food_name] = item_dict

    return render(request, 'grocery_list_app/grocery_list_2.html', {'form': form, 'data': food_dict})



