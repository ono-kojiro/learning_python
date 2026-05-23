# myapp/models/netif.py
from django.db import models
from .device import Device

class NetIf(models.Model):
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=32, blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="netifs")

    def __str__(self):
        return f"{self.device.name}:{self.name}"

