# myapp/models/ipaddress.py
from django.db import models

class IPAddress(models.Model):
    address = models.GenericIPAddressField(protocol="both", unpack_ipv4=True)
    subnet = models.PositiveSmallIntegerField(default=24)

    def __str__(self):
        return f"{self.address}/{self.subnet}"

