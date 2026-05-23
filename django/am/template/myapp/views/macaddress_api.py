# myapp/views/macaddress_api.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from myapp.models import MacAddress, NetIf, IPAddress


@csrf_exempt
def macaddress_add_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        netif_id = data.get("netif_id")
        mac = data.get("mac")
        ip_ids = data.get("ip_address_ids", [])
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # 必須チェック
    if not netif_id or not mac:
        return JsonResponse({"error": "netif_id and mac are required"}, status=400)

    # NetIf の存在確認
    try:
        netif = NetIf.objects.get(id=netif_id)
    except NetIf.DoesNotExist:
        return JsonResponse({"error": "NetIf not found"}, status=404)
    
    # 既存チェック
    existing = MacAddress.objects.filter(netif=netif).first()
    if existing:
        return JsonResponse({
            "id": existing.id,
            "mac": existing.mac,
            "netif": existing.netif.id,
            "ip_addresses": [str(ip) for ip in existing.ip_addresses.all()],
            "status": "already_exists"
        })

    # MacAddress を作成（unique=False なので重複OK）
    mac_obj = MacAddress.objects.create(
        mac=mac,
        netif=netif,
    )

    # IPAddress の紐付け
    for ip_id in ip_ids:
        try:
            ip = IPAddress.objects.get(id=ip_id)
            mac_obj.ip_addresses.add(ip)
        except IPAddress.DoesNotExist:
            pass  # 無効な IP は無視

    return JsonResponse({
        "id": mac_obj.id,
        "mac": mac_obj.mac,
        "netif": mac_obj.netif.id,
        "ip_addresses": [str(ip) for ip in mac_obj.ip_addresses.all()],
    })

