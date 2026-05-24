# myapp/views/ipaddress_api.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import IPAddress

@csrf_exempt
def ipaddress_add_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        address = data.get("address")
        subnet = data.get("subnet", 24)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not address:
        return JsonResponse({"error": "address is required"}, status=400)

    ip = IPAddress.objects.create(address=address, subnet=subnet)

    return JsonResponse({
        "id": ip.id,
        "address": ip.address,
        "subnet": ip.subnet,
    })

@csrf_exempt
def ipaddress_detail_api(request, ipaddress_id):
    try:
        ip = IPAddress.objects.get(id=ipaddress_id)
    except IPAddress.DoesNotExist:
        return JsonResponse({"error": "IPAddress not found"}, status=404)
    
    if request.method == "GET":
        return JsonResponse(
            {
                "id": ip.id,
                "address": ip.address,
                "subnet": ip.subnet,
            }
        )
    
    if request.method == "DELETE":
        ip.delete()
        return JsonResponse(
            {"status": "deleted", "id": ipaddress_id }
        )

    return JsonResponse({"error": "GET or DELETE only"})

@csrf_exempt
def ipaddress_list_api(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=405)

    ips = IPAddress.objects.all().order_by("id")

    data = []
    for ip in ips:
        data.append({
            "id": ip.id,
            "address": ip.address,
            "subnet": ip.subnet,
        })

    return JsonResponse({"ipaddresses": data})

