from django.urls import path
from .views import MessageListView, MessageDetailView, create_message

urlpatterns = [
    path('', MessageListView.as_view(), name='message-list'),
    path('<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('create/', create_message, name='message-create'),
]

