# myapp/admin/macaddress_admin.py
from django.contrib import admin
from myapp.models import MacAddress

@admin.register(MacAddress)
class MacAddressAdmin(admin.ModelAdmin):
    list_display = ("id", "mac", "netif", "ip_list")
    search_fields = ("mac", "netif__name", "netif__device__name")
    list_filter = ("netif__device",)

    def ip_list(self, obj):
        return ", ".join([str(ip) for ip in obj.ip_addresses.all()])
    ip_list.short_description = "IP Addresses"

