from django.urls import path
from .views import (
    SubscriptionView, create_payment_intent, confirm_payment,
    payfast_notify, PaymentHistoryView, get_stripe_key
)

urlpatterns = [
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('create-intent/', create_payment_intent, name='create-payment-intent'),
    path('confirm/', confirm_payment, name='confirm-payment'),
    path('payfast/notify/', payfast_notify, name='payfast-notify'),
    path('history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('stripe-key/', get_stripe_key, name='stripe-key'),
]

