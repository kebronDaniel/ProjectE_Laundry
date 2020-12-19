from django.urls import path,include
from .views import item_list,item,checkout


urlpatterns = [
    path('',item_list, name = 'item-list'),
    path('product/',item, name = 'item'),
    path('checkout/', checkout, name = 'checkout')
]
