from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'stock', 'balance', 'is_deleted')
    search_fields = ('code', 'name')
