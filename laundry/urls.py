from django.urls import path,include
from .views import checkout,HomeView,ItemDetailView


urlpatterns = [
    path('',HomeView.as_view(), name = 'item-list'),
    path('item/<slug>/',ItemDetailView.as_view(), name = 'item'),
    path('checkout/', checkout, name = 'checkout')
]
