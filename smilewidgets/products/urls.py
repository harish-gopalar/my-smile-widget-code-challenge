from django.urls import path
from . import views


urlpatterns = [

    path('get-price', views.GetPrice, name='get-price'),

]