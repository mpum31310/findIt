import hashlib
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Payment, Subscription


def _payfast_configured():
    return bool(settings.PAYFAST_MERCHANT_ID and settings.PAYFAST_MERCHANT_KEY)


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
        'notify_url': request.build_absolute_uri(reverse('payfast-notify')),
        'm_payment_id': str(payment_reference),
        'amount': format(Decimal(str(amount)).quantize(Decimal('0.01')), '.2f'),
        'item_name': item_name,
        'email_address': request.user.email or '',
        'custom': custom,
    }
    params['signature'] = _generate_payfast_signature(params)
    return params


def _subscription_context(request, subscription, **extra):
    return {
        'subscription': subscription,
        'payfast_url': settings.PAYFAST_URL,
        'plan_price': settings.SUBSCRIPTION_PRICE_DISPLAY,
        'payfast_configured': _payfast_configured(),
        'stripe_configured': _payfast_configured(),
        **extra,
    }


@login_required
def subscription_view(request):
    subscription, _ = Subscription.objects.get_or_create(user=request.user)
    subscription.check_status()
    context = _subscription_context(request, subscription)

    payment_status = request.GET.get('payment_status')
    payment_id = request.GET.get('m_payment_id')
    if payment_status == 'COMPLETE' and payment_id:
        payment = Payment.objects.filter(pk=payment_id, user=request.user).first()
        if payment:
            payment.status = 'completed'
            payment.save(update_fields=['status'])
        subscription.activate(duration_days=365)
        messages.success(request, 'Subscription activated. Thank you!')

    if request.method == 'POST' and 'subscribe' in request.POST:
        if not _payfast_configured():
            messages.error(
                request,
                'Payments are not configured yet. Add Payfast credentials to your .env file.',
            )
            return render(request, 'subscription.html', context)

        try:
            payment = Payment.objects.create(
                user=request.user,
                amount=settings.SUBSCRIPTION_PRICE / 100,
                status='pending',
                stripe_payment_intent_id='pending',
            )
            payfast_form_fields = _build_payfast_form(
                request,
                settings.SUBSCRIPTION_PRICE / 100,
                'Scanofinder annual subscription',
                f'subscription:{subscription.id}:{request.user.id}',
                request.build_absolute_uri(reverse('subscription')),
                request.build_absolute_uri(reverse('subscription')),
                payment.id,
            )
            context['payfast_form_fields'] = payfast_form_fields
            context['payment_id'] = payment.id
        except Exception as exc:
            messages.error(request, f'Could not start checkout: {exc}')

    return render(request, 'subscription.html', context)


@login_required
@require_POST
def confirm_subscription_view(request):
    payment_id = request.POST.get('payment_id') or request.POST.get('m_payment_id')
    if not payment_id:
        messages.error(request, 'Invalid payment request.')
        return redirect('subscription')

    payment = Payment.objects.filter(pk=payment_id, user=request.user).first()
    if payment:
        payment.status = 'completed'
        payment.save(update_fields=['status'])

    subscription, _ = Subscription.objects.get_or_create(user=request.user)
    subscription.activate(duration_days=365)
    messages.success(request, 'Subscription activated. Thank you!')

    return redirect('subscription')
