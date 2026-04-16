from django.urls import path
from .views import product_list_view, product_detail_view

app_name = 'products'

urlpatterns = [
    path('', product_list_view, name='product-list'),
    path('<int:product_id>', product_detail_view, name='product-detail')
]