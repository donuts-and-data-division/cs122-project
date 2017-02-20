from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
# Register your models here.
from .models import SnapLocations

admin.site.register(SnapLocations)