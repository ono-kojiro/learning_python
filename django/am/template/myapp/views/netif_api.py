# myapp/views/netif_api.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import NetIf, Device

@csrf_exempt
def netif_add_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        device_id = data.get("device_id")
        name = data.get("name")
        mac = data.get("mac_address")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not device_id or not name:
        return JsonResponse({"error": "device_id and name are required"}, status=400)

    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return JsonResponse({"error": "Device not found"}, status=404)

    netif = NetIf.objects.create(device=device, name=name, mac_address=mac)

    return JsonResponse({
        "id": netif.id,
        "device": netif.device.id,
        "name": netif.name,
        "mac_address": netif.mac_address,
    })


@csrf_exempt
def netif_delete_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        netif_id = data.get("id")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not netif_id:
        return JsonResponse({"error": "id is required"}, status=400)

    try:
        netif = NetIf.objects.get(id=netif_id)
    except NetIf.DoesNotExist:
        return JsonResponse({"error": "NetIf not found"}, status=404)

    netif.delete()

    return JsonResponse({"status": "deleted", "id": netif_id})

