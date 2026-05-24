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
    data = {}
    status = 200

    try:
        ip = IPAddress.objects.get(id=ipaddress_id)
    except IPAddress.DoesNotExist:
        return JsonResponse({"error": "IPAddress not found"}, status=404)
    
    if request.method == "GET":
        res = {
            "id": ip.id,
            "address": ip.address,
            "subnet": ip.subnet,
        }
    elif request.method == "DELETE":
        ip.delete()
        res = {"status": "deleted", "id": ipaddress_id }
    elif request.method in [ "PUT", "PATCH" ]:
        try:
            data = json.loads(request.body)
        except Exception:
            res = { "error": "Invalid JSON" }
            status = 400
            return JsonResponse(res, status=status)

        if "address" in data:
            ip.address = data["address"]

        if "subnet" in data:
            try:
                ip.subnet = int(data["subnet"])
            except ValueError:
                res = { "error": "Invalid subnet" }
                status = 400
                return JsonResponse(res, status=status)

        if "netif" in data:
            if data["netif"] is None:
                ip.netif = None
            else :
                try:
                    ip.netif_id = int(data["netif"])
                except ValueError:
                    res = { "error": "Invalid netif id" }
                    status = 400
                    return JsonResponse(res, status=status)

        if "macaddress" in data:
            if data["macaddress"] is None:
                ip.macaddress = None
            else :
                try:
                    ip.macaddress_id = int(data["macaddress"])
                except ValueError:
                    res = { "error": "Invalid macaddress id" }
                    status = 400
                    return JsonResponse(res, status=status)

        ip.save()
        res = {
            "id": ip.id,
            "address": ip.address,
            "subnet": ip.subnet,
            "netif": ip.netif.id if ip.netif else None,
            "macaddress": ip.macaddress.id if ip.macaddress else None,
        }
    elif request.method == "DELETE":
        ip.delete()
        res = { "status": "deleted", "id": ipaddress_id }
    else :
        res = {"error": "GET or DELETE only"}
        status = 405

    return JsonResponse(res, status=status)

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

