# myapp/views/device_api.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Device
from myapp.models import NetIf
from myapp.models import MacAddress

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
def device_detail_api(request, device_id):
    data = {}
    status = None
    
    if not device_id:
        return JsonResponse({"error": "device_id is required"}, status=400)

    try:
        device = Device.objects.get(id=device_id)
    except Device.DoesNotExist:
        return JsonResponse({"error": "Device not found"}, status=404)

    if request.method == "GET":
        data = {
            "id": device.id,
            "name": device.name,
            "serial_number": device.serial_number,
        }
        state = 200
    elif request.method == "DELETE":
        device.delete()
        data = { "status": "deleted", "id": device_id}
        status = 200
    else :
        data = {"error": "GET or DELETE only"}
        status = 405

    return JsonResponse(data, status=status)

@csrf_exempt
def device_list_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=405)

    devices = Device.objects.all().order_by("id")

    data = []
    for d in devices:
        data.append({
            "id": d.id,
            "name": d.name,
            "serial": d.serial_number,
        })

    return JsonResponse({"devices": data})

@csrf_exempt
def device_tree_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=405)

    devices = Device.objects.all().order_by("id")

    result = []

    for d in devices:
        device_entry = {
            "id": d.id,
            "name": d.name,
            "serial_number": d.serial_number,
            "netifs": []
        }

        # Device → NetIf
        netifs = NetIf.objects.filter(device=d).order_by("id")
        for n in netifs:
            netif_entry = {
                "id": n.id,
                "name": n.name,
                "mac_address": n.mac_address,
                "mac": None,
            }

            # NetIf → MacAddress（OneToOne）
            try:
                mac = MacAddress.objects.get(netif=n)
                mac_entry = {
                    "id": mac.id,
                    "mac": mac.mac,
                    "ip_addresses": [str(ip) for ip in mac.ip_addresses.all()],
                }
                netif_entry["mac"] = mac_entry
            except MacAddress.DoesNotExist:
                netif_entry["mac"] = None

            device_entry["netifs"].append(netif_entry)

        result.append(device_entry)

    return JsonResponse({"devices": result})

