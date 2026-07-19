from rest_framework import serializers
from .models import Subscription, Payment


class SubscriptionSerializer(serializers.ModelSerializer):
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'is_active', 'start_date', 'end_date', 'days_remaining', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_days_remaining(self, obj):
        if obj.is_active and obj.end_date:
            from django.utils import timezone
            delta = obj.end_date - timezone.now()
            return max(0, delta.days)
        return 0


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'amount', 'status', 'created_at')
        read_only_fields = ('id', 'created_at')

