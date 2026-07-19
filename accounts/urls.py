from django.urls import path
from .views import register, login, ProfileView, ProfileUpdateView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
]

