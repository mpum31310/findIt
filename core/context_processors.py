from decimal import Decimal

from django.conf import settings


def shop(request):
    context = {
        'plan_price': getattr(settings, 'SUBSCRIPTION_PRICE_DISPLAY', '200'),
        'cart_count': 0,
        'cart_total': Decimal('0.00'),
    }
    try:
        from shop.cart import get_cart_items
        cart_items, cart_total = get_cart_items(request.session)
        context['cart_count'] = sum(i['quantity'] for i in cart_items)
        context['cart_total'] = cart_total
    except Exception:
        pass

    if request.user.is_authenticated:
        try:
            from payments.models import Subscription
            subscription, _ = Subscription.objects.get_or_create(user=request.user)
            subscription.check_status()
            context['subscription'] = subscription
        except Exception:
            context['subscription'] = None
    return context
