from django.contrib import admin
from .models import User, Address

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'phone', 'created_at')
    search_fields = ('email', 'full_name')

admin.site.register(Address)