from django.urls import path
from .views import register_view, user_detail_view, user_update_view, logout_view, address_create_view, address_list_view, address_update_view

app_name = 'users'

urlpatterns = [
    path('register', register_view, name='register'),
    path('me', user_detail_view, name='user-detail'),
    path('update', user_update_view, name='user-update'),
    path('logout', logout_view, name='logout'),
    path('address', address_create_view, name='address-create'),
    path('address/list', address_list_view, name='address-list'),
    path('address/update/<int:address_id>', address_update_view, name='address-update'),
]