from django.urls import path
from . import views


urlpatterns = [

    path('get-price', views.get_price_details, name='get-price'),

]