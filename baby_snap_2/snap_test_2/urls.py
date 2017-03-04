from django.views.generic import TemplateView
from django.conf.urls import url
from djgeojson.views import GeoJSONLayerView
from .models import SnapLocations
from . import views


urlpatterns = [
    url(r'^auto$', views.auto),
    url(r'^auto2$', views.auto2),
    url(r'^ajax/get_places/$', views.get_places),
    url(r'^prices$', views.prices),
    url(r'^groceries$', views.groceries),
]

