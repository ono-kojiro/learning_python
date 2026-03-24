#from django.urls import path
#from .views_api import DeviceListCreateAPIView, DeviceDeleteAPIView
#from .views_api import NICListCreateAPIView, NICDeleteAPIView
#
#urlpatterns = [
#    path('devices/', DeviceListCreateAPIView.as_view(), name='api_device_list_create'),
#    path('devices/<int:pk>/', DeviceDeleteAPIView.as_view(), name='api_device_delete'),
#
#    path('nics/', NICListCreateAPIView.as_view(), name='api_nic_list_create'),
#    path('nics/<int:pk>/', NICDeleteAPIView.as_view(), name='api_nic_delete'),
#]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import DeviceViewSet, NICViewSet

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'nics', NICViewSet)

urlpatterns = [
    path('', include(router.urls)),
]




