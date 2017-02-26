from django.views.generic import TemplateView
from django.conf.urls import url
from djgeojson.views import GeoJSONLayerView
from .models import SnapLocations
from . import views


urlpatterns = [
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=SnapLocations), name='data'),
    url(r'^$', views.index, name='index'),
    url(r'^gmap$', views.gmap),
    url(r'^prettygmap$', views.prettygmap),
    url(r'^geojs$', views.geojs),
    url(r'^snapdata$', views.snapdata),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
]

