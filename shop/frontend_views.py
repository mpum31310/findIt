import hashlib
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from payments.models import Payment
from .cart import add_to_cart, clear_cart, get_cart_items, set_cart_quantity
from .forms import CheckoutForm, ProductForm
from .models import Order, OrderItem, Product


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


def shop_catalog_view(request):
    products = Product.objects.filter(is_active=True)
    context = {
        'label_products': products.filter(category=Product.CATEGORY_LABELS),
        'stamp_products': products.filter(category=Product.CATEGORY_STAMPS),
        'cart_items': [],
        'cart_total': Decimal('0.00'),
        'cart_count': 0,
        'payfast_configured': _payfast_configured(),
        'stripe_configured': _payfast_configured(),
    }
    cart_items, cart_total = get_cart_items(request.session)
    context['cart_items'] = cart_items
    context['cart_total'] = cart_total
    context['cart_count'] = sum(i['quantity'] for i in cart_items)
    return render(request, 'shop/catalog.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if request.method == 'POST' and 'add_to_cart' in request.POST:
        try:
            qty = int(request.POST.get('quantity', 1))
        except ValueError:
            qty = 1
        add_to_cart(request.session, product.id, max(1, qty))
        messages.success(request, f'Added {qty}× {product.name} to your cart.')
        return redirect('shop_product_detail', slug=product.slug)

    related_products = (
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(pk=product.pk)[:3]
    )
    cart_items, cart_total = get_cart_items(request.session)
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_count': sum(i['quantity'] for i in cart_items),
    })


@staff_member_required
def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added to the shop.')
            return redirect('shop_product_detail', slug=product.slug)
    else:
        form = ProductForm()
    return render(request, 'shop/product_add.html', {'form': form})


@require_POST
def cart_add_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    qty = int(request.POST.get('quantity', 1))
    add_to_cart(request.session, product.id, max(1, qty))
    messages.success(request, f'Added {product.name} to your cart.')
    next_url = request.POST.get('next', 'shop')
    if next_url == 'home':
        return redirect('home')
    if next_url == 'product':
        return redirect('shop_product_detail', slug=product.slug)
    return redirect('shop')


@login_required
def cart_view(request):
    cart_items, cart_total = get_cart_items(request.session)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('qty_'):
                product_id = int(key.replace('qty_', ''))
                try:
                    qty = int(value)
                except ValueError:
                    qty = 0
                set_cart_quantity(request.session, product_id, qty)
        if 'update_cart' in request.POST:
            messages.success(request, 'Cart updated.')
            return redirect('cart')
        if 'checkout' in request.POST and cart_items:
            return redirect('shop_checkout')

    cart_items, cart_total = get_cart_items(request.session)
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


@login_required
def checkout_view(request):
    cart_items, cart_total = get_cart_items(request.session)
    if not cart_items:
        messages.info(request, 'Your cart is empty.')
        return redirect('shop')

    if request.method == 'GET':
        form = CheckoutForm(user=request.user)
    else:
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid() and 'place_order' in request.POST:
            order = Order.objects.create(
                user=request.user,
                total=cart_total,
                shipping_name=form.cleaned_data['shipping_name'],
                shipping_phone=form.cleaned_data['shipping_phone'],
                shipping_address=form.cleaned_data['shipping_address'],
                notes=form.cleaned_data.get('notes', ''),
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    unit_price=item['product'].price,
                )

            clear_cart(request.session)

            if _payfast_configured():
                try:
                    payment = Payment.objects.create(
                        user=request.user,
                        amount=cart_total,
                        status='pending',
                        stripe_payment_intent_id=str(order.pk),
                    )
                    order.stripe_payment_intent_id = str(payment.id)
                    order.save(update_fields=['stripe_payment_intent_id'])
                    payfast_form = _build_payfast_form(
                        request,
                        cart_total,
                        f'Order #{order.pk}',
                        f'order:{order.pk}:{request.user.id}',
                        request.build_absolute_uri(reverse('shop_order_detail', kwargs={'pk': order.pk})),
                        request.build_absolute_uri(reverse('shop_checkout')),
                        payment.id,
                    )
                    return render(request, 'shop/checkout_pay.html', {
                        'order': order,
                        'payfast_form_fields': payfast_form,
                        'payfast_url': settings.PAYFAST_URL,
                        'payfast_configured': True,
                    })
                except Exception as exc:
                    messages.warning(
                        request,
                        f'Order #{order.pk} created but online payment failed: {exc}. '
                        'We will contact you to arrange payment.',
                    )
                    order.status = Order.STATUS_PROCESSING
                    order.save(update_fields=['status'])
                    return redirect('shop_order_detail', pk=order.pk)

            order.status = Order.STATUS_PROCESSING
            order.save(update_fields=['status'])
            messages.success(
                request,
                f'Order #{order.pk} placed! We will confirm delivery details shortly.',
            )
            return redirect('shop_order_detail', pk=order.pk)

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'payfast_configured': _payfast_configured(),
        'stripe_configured': _payfast_configured(),
    })


@login_required
@require_POST
def confirm_order_payment_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    payment_id = request.POST.get('payment_id') or request.POST.get('m_payment_id')
    if not payment_id:
        messages.error(request, 'Invalid payment.')
        return redirect('shop_order_detail', pk=pk)

    payment = Payment.objects.filter(pk=payment_id, user=request.user).first()
    if payment:
        payment.status = 'completed'
        payment.save(update_fields=['status'])

    order.status = Order.STATUS_PAID
    order.save(update_fields=['status'])
    messages.success(request, 'Payment received. Thank you for your order!')

    return redirect('shop_order_detail', pk=pk)


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    payment_id = request.GET.get('m_payment_id')
    payment_status = request.GET.get('payment_status')

    if payment_status == 'COMPLETE' and payment_id:
        payment = Payment.objects.filter(pk=payment_id, user=request.user).first()
        if payment:
            payment.status = 'completed'
            payment.save(update_fields=['status'])
        if order.status == Order.STATUS_PENDING:
            order.status = Order.STATUS_PAID
            order.save(update_fields=['status'])
            messages.success(request, 'Payment received. Thank you for your order!')

    return render(request, 'shop/order_detail.html', {'order': order})
