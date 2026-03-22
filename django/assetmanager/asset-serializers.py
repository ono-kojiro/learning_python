from rest_framework import serializers
from .models import Device
from .models import NIC

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'serial_number']

class NICSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIC
        fields = ['id', 'device', 'name', 'description']


