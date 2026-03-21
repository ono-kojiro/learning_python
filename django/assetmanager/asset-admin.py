from django.contrib import admin
from .models import Device, NIC

class NICInline(admin.TabularInline):
    model = NIC
    extra = 1

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    inlines = [NICInline]
    list_display = ('name', 'serial_number')

@admin.register(NIC)
class NICAdmin(admin.ModelAdmin):
    list_display = ('device', 'name', 'description')


