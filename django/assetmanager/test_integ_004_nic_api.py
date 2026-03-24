import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://192.168.1.72:8000"

CA_CERT = "/home/kojiro/devel/learning_python/django/assetmanager/myrootca.crt"

def test_create_nic():
    url = BASE_URL + "/api/nics/"

    payload = {
        "device_id": None,
        "name": "eth0",
        "serial_number": "DEF456"
    }

    # POST で Device を作成
    r = requests.post(url, json=payload, verify=CA_CERT)
    assert r.status_code == 201

    # GET で作成されたことを確認
    r2 = requests.get(url, verify=False)
    assert r2.status_code == 200

    devices = r2.json()
    assert any(d["name"] == "eth0" for d in devices)


