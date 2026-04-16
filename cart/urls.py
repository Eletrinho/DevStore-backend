from django.urls import path
from .views import cart_view, add_to_cart_view, remove_from_cart_view

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add', add_to_cart_view, name='add-to-cart'),
    path('remove', remove_from_cart_view, name='remove-from-cart')
]