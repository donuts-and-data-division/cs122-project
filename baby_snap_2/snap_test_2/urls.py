from django.views.generic import TemplateView
from django.conf.urls import url
from djgeojson.views import GeoJSONLayerView
from .models import SnapLocations
from . import views


urlpatterns = [
    url(r'^auto$', views.auto),
    url(r'^auto2$', views.auto2),
    url(r'^ajax/get_places/$', views.get_places),
    url(r'^ajax/go_to_prices$', views.prices),
    url(r'^groceries/(?P<place_id>\w+)/$', views.submit_grocery_list, name='grocery_list'),
    url(r'^prices$', views.prices),
    url(r'^groceries$', views.submit_grocery_list, name='grocery_list'),
    url(r'^ajax/cash_register/$', views.cash_register, name='cash_register'),
    url(r'^submit-prices$', views.submit_prices, name='submit_prices'),
<<<<<<< HEAD
    url(r'^submit-prices/(?P<place_id>\w+)/(?P<food_string>[\d+&?]+)/$', views.submit_prices, name='price_page'),
    url(r'^submit-prices/(?P<place_id>\w+)/$', views.submit_prices_blank, name='blank_price_page'),
    
=======
>>>>>>> 6971b8ff72b87c87feff027ee1665c8e7820129d
]

