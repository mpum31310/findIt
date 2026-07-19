from decimal import Decimal

from django.db import migrations


def seed_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    products = [
        {
            'name': 'Waterproof QR Label Sheet',
            'slug': 'qr-labels-20',
            'category': 'labels',
            'description': (
                'Pre-cut adhesive labels ready for your Scanofinder QR codes. '
                'Water-resistant vinyl — ideal for lunchboxes, books, and stationery.'
            ),
            'price': Decimal('89.00'),
            'pack_size': '20 labels per sheet',
            'sort_order': 1,
        },
        {
            'name': 'Family QR Label Pack',
            'slug': 'qr-labels-50',
            'category': 'labels',
            'description': (
                'Larger pack for families with many items. Same durable material, '
                'peel-and-stick application. Print your codes from the app and apply.'
            ),
            'price': Decimal('179.00'),
            'pack_size': '50 labels per pack',
            'sort_order': 2,
        },
        {
            'name': 'Mini QR Stickers',
            'slug': 'qr-stickers-15',
            'category': 'labels',
            'description': (
                'Small round stickers for bottles, earbuds, and narrow surfaces. '
                'Pairs with your generated QR codes.'
            ),
            'price': Decimal('69.00'),
            'pack_size': '15 stickers',
            'sort_order': 3,
        },
        {
            'name': 'QR Clothing Stamp Kit',
            'slug': 'qr-stamp-kit',
            'category': 'stamps',
            'description': (
                'Custom stamp kit to mark fabric items — shirts, bags, and hats. '
                'Includes stamp, ink pad, and alignment guide for clear QR prints.'
            ),
            'price': Decimal('249.00'),
            'pack_size': '1 complete kit',
            'sort_order': 10,
        },
        {
            'name': 'QR Stamp Refill Ink',
            'slug': 'qr-stamp-ink',
            'category': 'stamps',
            'description': (
                'Replacement fabric ink for your Scanofinder clothing stamp. '
                'Wash-resistant formula for school uniforms and sports gear.'
            ),
            'price': Decimal('79.00'),
            'pack_size': '1 ink bottle',
            'sort_order': 11,
        },
        {
            'name': 'Heavy-Duty QR Stamp',
            'slug': 'qr-stamp-heavy',
            'category': 'stamps',
            'description': (
                'Extra-durable stamp for thick fabrics and backpacks. '
                'Larger print area for maximum scan reliability.'
            ),
            'price': Decimal('299.00'),
            'pack_size': '1 stamp + ink',
            'sort_order': 12,
        },
    ]
    for data in products:
        Product.objects.update_or_create(slug=data['slug'], defaults=data)


def unseed_products(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Product.objects.filter(
        slug__in=[
            'qr-labels-20', 'qr-labels-50', 'qr-stickers-15',
            'qr-stamp-kit', 'qr-stamp-ink', 'qr-stamp-heavy',
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_products, unseed_products),
    ]
