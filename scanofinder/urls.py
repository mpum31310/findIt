"""
URL configuration for scanofinder project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core.views import home_view, about_view, terms_view, privacy_view
from accounts.frontend_views import register_view, login_view, profile_view
from items.frontend_views import items_list_view, item_add_view, item_detail_view, item_scan_view
from item_messages.frontend_views import messages_list_view, message_detail_view
from children.frontend_views import children_list_view, child_add_view, child_detail_view
from payments.frontend_views import subscription_view, confirm_subscription_view
from shop.frontend_views import (
    shop_catalog_view, product_detail_view, product_add_view,
    cart_add_view, cart_view, checkout_view,
    confirm_order_payment_view, order_detail_view,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Frontend views
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('terms/', terms_view, name='terms'),
    path('privacy/', privacy_view, name='privacy'),
    
    # Authentication
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),

    # Children
    path('children/', children_list_view, name='children_list'),
    path('children/add/', child_add_view, name='child_add'),
    path('children/<int:pk>/', child_detail_view, name='child_detail'),

    # Items
    path('items/', items_list_view, name='items_list'),
    path('items/add/', item_add_view, name='item_add'),
    path('items/<int:pk>/', item_detail_view, name='item_detail'),
    path('scan/<str:qr_data>/', item_scan_view, name='item_scan'),
    
    # Messages
    path('messages/', messages_list_view, name='messages_list'),
    path('messages/<int:pk>/', message_detail_view, name='message_detail'),

    # Shop (physical QR labels & stamps)
    path('shop/', shop_catalog_view, name='shop'),
    path('shop/add/', product_add_view, name='shop_product_add'),
    path('shop/product/<slug:slug>/', product_detail_view, name='shop_product_detail'),
    path('shop/cart/', cart_view, name='cart'),
    path('shop/cart/add/<int:product_id>/', cart_add_view, name='cart_add'),
    path('shop/checkout/', checkout_view, name='shop_checkout'),
    path('shop/orders/<int:pk>/', order_detail_view, name='shop_order_detail'),
    path('shop/orders/<int:pk>/pay/confirm/', confirm_order_payment_view, name='shop_confirm_payment'),

    # App subscription (optional annual plan)
    path('subscription/', subscription_view, name='subscription'),
    path('subscription/confirm/', confirm_subscription_view, name='subscription_confirm'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
