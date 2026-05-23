# myapp/admin/ipaddress_admin.py
from django.contrib import admin
from myapp.models import IPAddress

@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "address", "subnet")

