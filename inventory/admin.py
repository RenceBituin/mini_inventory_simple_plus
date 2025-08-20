from django.contrib import admin
from .models import Item, Category

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'quantity', 'price', 'value', 'updated_at')
    search_fields = ('name', 'sku')
    list_filter = ('category', 'updated_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
