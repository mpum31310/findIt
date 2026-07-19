import hashlib
from decimal import Decimal

from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Subscription, Payment
from .serializers import SubscriptionSerializer, PaymentSerializer


def _generate_payfast_signature(data):
    payload = {k: v for k, v in data.items() if v not in (None, "")}
    if settings.PAYFAST_PASSPHRASE:
        payload['passphrase'] = settings.PAYFAST_PASSPHRASE
    signature_string = '&'.join(f'{key}={payload[key]}' for key in sorted(payload))
    return hashlib.md5(signature_string.encode('utf-8')).hexdigest()


def _build_payfast_form(request, amount, item_name, custom, return_url, cancel_url, payment_reference):
    params = {
        'merchant_id': settings.PAYFAST_MERCHANT_ID,
        'merchant_key': settings.PAYFAST_MERCHANT_KEY,
        'return_url': return_url,
        'cancel_url': cancel_url,
        'notify_url': request.build_absolute_uri('/payments/payfast/notify/'),
        'm_payment_id': str(payment_reference),
        'amount': format(Decimal(str(amount)).quantize(Decimal('0.01')), '.2f'),
        'item_name': item_name,
        'email_address': request.user.email or '',
        'custom': custom,
    }
    params['signature'] = _generate_payfast_signature(params)
    return params


@api_view(['GET'])
@permission_classes([AllowAny])
def get_stripe_key(request):
    """Get Payfast configuration for the frontend."""
    return Response({
        'merchant_id': settings.PAYFAST_MERCHANT_ID,
        'merchant_key': settings.PAYFAST_MERCHANT_KEY,
        'payfast_url': settings.PAYFAST_URL,
    })


class SubscriptionView(generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        subscription, created = Subscription.objects.get_or_create(user=self.request.user)
        subscription.check_status()
        return subscription


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    """Create a Payfast checkout form for subscription."""
    try:
        amount = settings.SUBSCRIPTION_PRICE / 100
        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            status='pending',
            stripe_payment_intent_id='pending',
        )
        form_fields = _build_payfast_form(
            request,
            amount,
            'Scanofinder annual subscription',
            f'subscription:{subscription.id}:{request.user.id}',
            request.build_absolute_uri('/subscription/'),
            request.build_absolute_uri('/subscription/'),
            payment.id,
        )
        return Response({
            'payfast_url': settings.PAYFAST_URL,
            'payfast_form_fields': form_fields,
            'payment_id': payment.id,
            'amount': amount,
        })
    except Exception as exc:
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    """Confirm payment and activate subscription."""
    payment_id = request.data.get('payment_id') or request.data.get('m_payment_id')

    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
        payment.status = 'completed'
        payment.save()

        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        subscription.activate(duration_days=365)

        return Response({
            'message': 'Payment confirmed and subscription activated',
            'subscription': SubscriptionSerializer(subscription).data,
        })
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as exc:
        return Response({'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def payfast_notify(request):
    """Handle Payfast callback notifications."""
    payment_status = request.POST.get('payment_status')
    payment_id = request.POST.get('m_payment_id')
    custom = request.POST.get('custom', '')

    if payment_id:
        payment = Payment.objects.filter(pk=payment_id).first()
        if payment:
            payment.status = 'completed' if payment_status == 'COMPLETE' else 'failed'
            payment.save(update_fields=['status'])

    if custom.startswith('subscription:'):
        user_id = custom.split(':')[-1]
        subscription, _ = Subscription.objects.get_or_create(user_id=user_id)
        if payment_status == 'COMPLETE':
            subscription.activate(duration_days=365)

    return HttpResponse('OK')


class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

