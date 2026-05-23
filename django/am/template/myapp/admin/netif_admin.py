# myapp/admin/netif_admin.py
from django.contrib import admin
from myapp.models import NetIf

@admin.register(NetIf)
class NetIfAdmin(admin.ModelAdmin):
    list_display = ("id", "device", "name", "mac_address")

