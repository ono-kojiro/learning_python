#from rest_framework import generics
from rest_framework import viewsets

from .models import Device
from .serializers import DeviceSerializer

from .models import NIC
from .serializers import NICSerializer

#class DeviceListCreateAPIView(generics.ListCreateAPIView):
#    queryset = Device.objects.all()
#    serializer_class = DeviceSerializer

#class DeviceDeleteAPIView(generics.DestroyAPIView):
#    queryset = Device.objects.all()
#    serializer_class = DeviceSerializer

#class NICListCreateAPIView(generics.ListCreateAPIView):
#    queryset = NIC.objects.all()
#    serializer_class = NICSerializer

#class NICDeleteAPIView(generics.DestroyAPIView):
#    queryset = NIC.objects.all()
#    serializer_class = NICSerializer

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class NICViewSet(viewsets.ModelViewSet):
    queryset = NIC.objects.all()
    serializer_class = NICSerializer


