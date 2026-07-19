from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from payments.models import Subscription
import re


class SubscriptionMiddleware(MiddlewareMixin):
    """Check if user has active subscription for protected endpoints"""
    
    # Exclude these paths from subscription check
    EXCLUDED_PATHS = [
        '/api/auth/register',
        '/api/auth/login',
        '/api/auth/profile',
        '/api/items/qr/',
        '/api/messages/create/',
        '/api/payments/history',
        '/admin/',
        '/static/',
        '/media/',
    ]
    
    # These paths require subscription
    PROTECTED_PATHS = [
        '/api/children/',
        '/api/items/',
        '/api/payments/subscription',
        '/api/payments/create-intent',
        '/api/payments/confirm',
    ]
    
    def process_request(self, request):
        # Skip check for excluded paths
        for excluded in self.EXCLUDED_PATHS:
            if request.path.startswith(excluded):
                return None
        
        # Only check protected paths
        is_protected = False
        for protected in self.PROTECTED_PATHS:
            if request.path.startswith(protected):
                is_protected = True
                break
        
        if is_protected and request.user.is_authenticated:
            try:
                subscription = Subscription.objects.get(user=request.user)
                if not subscription.check_status():
                    return JsonResponse({
                        'error': 'Subscription expired. Please renew your subscription.',
                        'subscription_required': True
                    }, status=403)
            except Subscription.DoesNotExist:
                return JsonResponse({
                    'error': 'Active subscription required. Please subscribe to continue.',
                    'subscription_required': True
                }, status=403)
        
        return None

