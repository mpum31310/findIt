import os
os.chdir(r'c:\Users\Mpumelelo\Documents\websites\Scanofinder django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scanofinder.settings')
import django
django.setup()
from django.test import RequestFactory
from core.views import home_view

class DummyUser:
    is_authenticated = False

req = RequestFactory().get('/')
req.user = DummyUser()

try:
    response = home_view(req)
    print('status', response.status_code)
    print(response.content[:200])
except Exception:
    import traceback
    traceback.print_exc()
