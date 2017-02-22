from django.shortcuts import render

# Create your views here.
def grocery_list(request):
    return render(request, 'grocery_list_app/grocery_list.html', {})