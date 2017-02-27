from django.shortcuts import render
from .forms import GroceryForm
from django.http import JsonResponse
# Create your views here.
#def grocery_list(request):
#    return render(request, 'grocery_list_app/grocery_list.html', {})

def submit_grocery_list(request):
    if request.method == "POST":
        form = GroceryForm(request.POST)
        if form.is_valid():
            grocery_list = form.save(commit=False)
            grocery_list.food_name = request.food_name
            grocery_list.date_last_created = timezone.now()
            grocery_list.quantity = request.food_quantity
            grocery_list.save()
            #return redirect('post_detail', pk=post.pk)
    else:
        form = GroceryForm()
    return render(request, 'grocery_list_app/grocery_list.html', {'form': form})



def grocery_money(request):
    food_name = request.GET.get('food_name', None)
    data = {
            'food_price': FoodPrices.objects.filter(food_name=food_name)
            #['food_price']
        }

    return JsonResponse(data)