from decimal import Decimal

from .models import Product


CART_SESSION_KEY = 'shop_cart'


def get_cart(session):
    return session.get(CART_SESSION_KEY, {})


def save_cart(session, cart):
    session[CART_SESSION_KEY] = cart
    session.modified = True


def add_to_cart(session, product_id, quantity=1):
    cart = get_cart(session)
    key = str(product_id)
    cart[key] = cart.get(key, 0) + quantity
    save_cart(session, cart)


def set_cart_quantity(session, product_id, quantity):
    cart = get_cart(session)
    key = str(product_id)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    save_cart(session, cart)


def clear_cart(session):
    session.pop(CART_SESSION_KEY, None)
    session.modified = True


def get_cart_items(session):
    cart = get_cart(session)
    if not cart:
        return [], Decimal('0.00')

    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)
    product_map = {p.id: p for p in products}

    items = []
    total = Decimal('0.00')
    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = product_map.get(pid)
        if not product:
            continue
        line_total = product.price * qty
        items.append({
            'product': product,
            'quantity': qty,
            'line_total': line_total,
        })
        total += line_total
    return items, total
