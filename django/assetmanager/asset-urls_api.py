from django.urls import path
from .views_api import DeviceListCreateAPIView, DeviceDeleteAPIView

urlpatterns = [
    path('devices/', DeviceListCreateAPIView.as_view(), name='api_device_list_create'),
    path('devices/<int:pk>/', DeviceDeleteAPIView.as_view(), name='api_device_delete'),
]


