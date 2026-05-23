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

