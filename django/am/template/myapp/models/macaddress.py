# myapp/models/macaddress.py
from django.db import models
from .netif import NetIf
from .ipaddress import IPAddress

class MacAddress(models.Model):
    mac = models.CharField(max_length=32)
    netif = models.OneToOneField(
        NetIf,
        on_delete=models.CASCADE,
        related_name="mac_obj"
    )
    ip_addresses = models.ManyToManyField(
        IPAddress,
        related_name="mac_addresses",
        blank=True
    )

    def __str__(self):
        return self.mac

