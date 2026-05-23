# myapp/admin/device_admin.py
from django.contrib import admin
from myapp.models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "serial_number")

