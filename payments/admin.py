from django.contrib import admin
from .models import Subscription, Payment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'start_date', 'end_date', 'created_at')
    list_filter = ('is_active', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')

