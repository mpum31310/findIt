from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'item', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender_name', 'sender_email', 'message')

