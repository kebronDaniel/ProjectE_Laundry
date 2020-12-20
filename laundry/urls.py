from django.urls import path,include
from .views import checkout,HomeView,ItemDetailView,add_to_cart,remove_from_cart


urlpatterns = [
    path('',HomeView.as_view(), name = 'item-list'),
    path('item/<slug>/',ItemDetailView.as_view(), name = 'item'),
    path('checkout/', checkout, name = 'checkout'),
    path('add-to-cart/<slug>/',add_to_cart, name = "add-to-cart"),
    path('remove-from-cart/<slug>/',remove_from_cart, name = "remove-from-cart"),
]
