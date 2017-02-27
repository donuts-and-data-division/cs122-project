from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.submit_grocery_list, name='grocery_list'),
    url(r'^ajax/cash_register/$', views.cash_register, name='cash_register'),
]