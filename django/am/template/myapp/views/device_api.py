# myapp/views/device_api.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Device

@csrf_exempt
def device_add_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        name = data.get("name")
        serial = data.get("serial_number")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not name:
        return JsonResponse({"error": "name is required"}, status=400)

    device = Device.objects.create(name=name, serial_number=serial)
    return JsonResponse({
        "id": device.id,
        "name": device.name,
        "serial_number": device.serial_number,
    })

@csrf_exempt
def device_delete_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        device_id = data.get("id")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not device_id:
        return JsonResponse({"error": "id is required"}, status=400)

    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return JsonResponse({"error": "Device not found"}, status=404)

    device.delete()

    return JsonResponse({"status": "deleted", "id": device_id})

