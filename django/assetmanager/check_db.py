# check_db.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asset_manager.settings")
django.setup()

from asset.models import Device, NIC

print("Devices:")
for d in Device.objects.all():
    print(d.id, d.name, d.serial_number)

print("\nNICs:")
for nic in NIC.objects.all():
    print(nic.id, nic.device.name, nic.name, nic.description)

