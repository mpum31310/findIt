from django.conf import settings
from django.shortcuts import render


def home_view(request):
    from shop.models import Product

    context = {
        'plan_price': getattr(settings, 'SUBSCRIPTION_PRICE_DISPLAY', '200'),
        'label_products': [],
        'stamp_products': [],
    }

    try:
        products = Product.objects.filter(is_active=True)
        context['label_products'] = products.filter(category=Product.CATEGORY_LABELS)
        context['stamp_products'] = products.filter(category=Product.CATEGORY_STAMPS)
    except Exception:
        context['label_products'] = []
        context['stamp_products'] = []

    if request.user.is_authenticated:
        try:
            from payments.models import Subscription
            subscription, _ = Subscription.objects.get_or_create(user=request.user)
            subscription.check_status()
            context['subscription'] = subscription
        except Exception:
            context['subscription'] = None
    return render(request, 'home.html', context)


def about_view(request):
    return render(request, 'about.html')


def terms_view(request):
    return render(request, 'terms.html')


def privacy_view(request):
    return render(request, 'privacy.html')
