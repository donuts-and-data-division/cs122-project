from django.views.generic import TemplateView
from django.conf.urls import url
from djgeojson.views import GeoJSONLayerView
from .models import SnapLocations
from . import views


urlpatterns = [
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=SnapLocations), name='data'),
    #url(r'^$', views.index, name='index'),
    url(r'^gmap$', views.gmap),
    url(r'^gmapdata$', views.gmapdata),
    url(r'^prettygmap$', views.prettygmap),
    url(r'^geojs$', views.geojs),
    url(r'^auto$', views.auto),
    url(r'^auto2$', views.auto2),
    url(r'^ajax/get_places/$', views.get_places),
    url(r'^ajax/go_to_prices$', views.prices),
    url(r'^groceries/(?P<place_id>\w+)/$', views.submit_grocery_list, name='grocery_list'),
    url(r'^ajax/cash_register/$', views.cash_register, name='cash_register'),
]

