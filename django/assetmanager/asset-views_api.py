from rest_framework import generics
from .models import Device
from .serializers import DeviceSerializer

class DeviceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class DeviceDeleteAPIView(generics.DestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

