from django.conf.urls import url
#from .models import SnapLocations
from . import views


urlpatterns = [
    url(r'^home$', views.home),
    url(r'^ajax/get_places/$', views.get_places),
    url(r'^groceries/(?P<store_id>\w+)/$', views.submit_grocery_list, name='grocery_list'),
    url(r'^ajax/cash_register/$', views.cash_register, name='cash_register'),
    url(r'^submit-prices$', views.submit_prices, name='submit_prices'),
    url(r'^submit-prices/(?P<store_id>\w+)/(?P<food_string>[\d+&?]+)/$', views.submit_prices, name='price_page'),
    url(r'^submit-prices/(?P<store_id>\w+)/$', views.submit_prices_blank, name='blank_price_page'),
    url(r'^ajax/update_price/$', views.update_price, name='update_price')
]

