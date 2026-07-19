from decimal import Decimal

from django.db import models
from accounts.models import User


class Product(models.Model):
    CATEGORY_LABELS = 'labels'
    CATEGORY_STAMPS = 'stamps'
    CATEGORY_CHOICES = [
        (CATEGORY_LABELS, 'QR Labels'),
        (CATEGORY_STAMPS, 'QR Stamps'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pack_size = models.CharField(
        max_length=100,
        help_text='e.g. "20 waterproof labels" or "1 stamp kit"',
    )
    image = models.ImageField(upload_to='shop/products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PAID = 'paid'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending payment'),
        (STATUS_PAID, 'Paid'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shop_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_name = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} — {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f'{self.quantity}× {self.product.name}'
