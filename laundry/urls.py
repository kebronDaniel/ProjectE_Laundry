from django.urls import path,include
from .views import item_list


urlpatterns = [
    path('',item_list, name = 'item-list'),
]
