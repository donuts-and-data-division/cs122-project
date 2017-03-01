from django.views.generic import TemplateView
from django.conf.urls import url
from djgeojson.views import GeoJSONLayerView
from .models import SnapLocations
from . import views


urlpatterns = [
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=SnapLocations), name='data'),
    url(r'^$', views.index, name='index'),
    url(r'^gmap$', views.gmap),
    url(r'^gmapdata$', views.gmapdata),
    url(r'^prettygmap$', views.prettygmap),
    url(r'^geojs$', views.geojs),
    url(r'^snapdata$', views.snapdata),
    url(r'^auto2$', views.auto2),
   # url(r'^auto$', views.auto),
    #url(r'^search_retailers$', views.search_retailers),
    url(r'^ajax/get_places/$', views.get_places)

]

