from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'child', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')

