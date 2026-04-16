from django.urls import path
from .views import checkout_view, order_history_view, order_detail_view, cancel_order_view

app_name = 'orders'

urlpatterns = [
    path('checkout', checkout_view, name='checkout'),
    path('history', order_history_view, name='order-history'),
    path('detail/<str:order_id>', order_detail_view, name='order-detail'),
    path('cancel/<str:order_id>', cancel_order_view, name='cancel-order')
]