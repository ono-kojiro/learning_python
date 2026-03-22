import requests

BASE_URL = "https://127.0.0.1:8000"

def test_create_nic():
    payload = {
        "device_id": 1,
        "name": "eth0",
        "description": "test nic"
    }

    r = requests.post(f"{BASE_URL}/api/nics/", json=payload)
    assert r.status_code == 201

    # GET で確認
    r2 = requests.get(f"{BASE_URL}/api/nics/")
    assert any(n["name"] == "eth0" for n in r2.json())


