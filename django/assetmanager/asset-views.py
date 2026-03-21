from django.shortcuts import render, redirect, get_object_or_404
from .models import Device

def index(request):
    return render(request, 'index.html')

def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})

def device_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        serial = request.POST.get('serial_number')
        Device.objects.create(name=name, serial_number=serial)
        return redirect('device_list')

    return render(request, 'device_add.html')

def device_delete(request, pk):
    device = get_object_or_404(Device, pk=pk)
    device.delete()
    return redirect('device_list')


