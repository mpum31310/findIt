from django.urls import path
from .views import ItemListCreateView, ItemDetailView, get_item_by_qr

urlpatterns = [
    path('', ItemListCreateView.as_view(), name='item-list-create'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('qr/<str:qr_data>/', get_item_by_qr, name='item-by-qr'),
]

