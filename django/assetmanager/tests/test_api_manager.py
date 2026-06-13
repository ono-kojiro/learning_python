import sys
import requests
import pytest


# ---------------------------------------------------------
# 1. GET /api/managers/ で一覧を取得
# ---------------------------------------------------------
@pytest.mark.order(10)
def test_get_managers(configs):
    url = f"{configs['base_url']}/api/managers/"
    print(url, file=sys.stderr)

    res = requests.get(url)
    assert res.status_code == 200

    data = res.json()
    print("MANAGERS:", data, file=sys.stderr)

    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]

    assert "id" in first
    assert "manager_id" in first
    assert "name" in first
    assert "email" in first
    assert "device_ids" in first

    assert isinstance(first["device_ids"], list)


# ---------------------------------------------------------
# 2. GET /api/devices/<id>/ で managers を確認
# ---------------------------------------------------------
@pytest.mark.order(11)
def test_get_device_managers(configs):
    # 一覧から Device の PK を取得
    url_list = f"{configs['base_url']}/api/devices/"
    print(url_list, file=sys.stderr)

    res_list = requests.get(url_list)
    assert res_list.status_code == 200

    devices = res_list.json()
    assert len(devices) > 0

    device_pk = devices[0]["id"]

    # 個別取得（lookup_field=id）
    url = f"{configs['base_url']}/api/devices/{device_pk}/"
    print(url, file=sys.stderr)

    res = requests.get(url)
    assert res.status_code == 200

    data = res.json()
    print("DEVICE:", data, file=sys.stderr)

    assert "managers" in data
    assert isinstance(data["managers"], list)


# ---------------------------------------------------------
# 3. PATCH /api/devices/<id>/ で managers を更新
# ---------------------------------------------------------
@pytest.mark.order(12)
def test_patch_device_managers(configs):
    # Device 一覧から PK を取得
    url_list = f"{configs['base_url']}/api/devices/"
    res_list = requests.get(url_list)
    assert res_list.status_code == 200

    devices = res_list.json()
    assert len(devices) > 0
    device_pk = devices[0]["id"]

    # PATCH
    url = f"{configs['base_url']}/api/devices/{device_pk}/"
    print(url, file=sys.stderr)

    payload = {
        "managers": [2, 3]
    }

    res = requests.patch(url, json=payload)
    print("PATCH RESULT:", res.json(), file=sys.stderr)

    assert res.status_code == 200

    data = res.json()
    assert data["managers"] == [2, 3]


# ---------------------------------------------------------
# 4. PATCH /api/managers/<pk>/ で devices を更新
# ---------------------------------------------------------
@pytest.mark.order(13)
def test_patch_manager_devices(configs):
    # Manager 一覧から PK を取得
    url_list = f"{configs['base_url']}/api/managers/"
    res_list = requests.get(url_list)
    assert res_list.status_code == 200

    managers = res_list.json()
    assert len(managers) > 0
    manager_pk = managers[0]["id"]

    # Device 一覧から PK を取得
    url_dev_list = f"{configs['base_url']}/api/devices/"
    res_dev_list = requests.get(url_dev_list)
    assert res_dev_list.status_code == 200

    devices = res_dev_list.json()
    assert len(devices) >= 2

    device_pks = [devices[0]["id"], devices[1]["id"]]

    # PATCH
    url = f"{configs['base_url']}/api/managers/{manager_pk}/"
    print(url, file=sys.stderr)

    payload = {
        "devices": device_pks
    }

    res = requests.patch(url, json=payload)
    print("PATCH RESULT:", res.json(), file=sys.stderr)

    assert res.status_code == 200

    data = res.json()
    assert data["devices"] == device_pks

    # Device 側にも反映されているか確認
    url2 = f"{configs['base_url']}/api/devices/{device_pks[0]}/"
    res2 = requests.get(url2)
    assert res2.status_code == 200

    assert manager_pk in res2.json()["managers"]


# ---------------------------------------------------------
# 5. Device に最低1人の Manager が必要な場合のテスト
# ---------------------------------------------------------
@pytest.mark.order(14)
def test_device_requires_at_least_one_manager(configs):
    # Device 一覧から PK を取得
    url_list = f"{configs['base_url']}/api/devices/"
    res_list = requests.get(url_list)
    assert res_list.status_code == 200

    devices = res_list.json()
    assert len(devices) > 0
    device_pk = devices[0]["id"]

    url = f"{configs['base_url']}/api/devices/{device_pk}/"
    print(url, file=sys.stderr)

    payload = {
        "managers": []
    }

    res = requests.patch(url, json=payload)
    print("PATCH RESULT:", res.json(), file=sys.stderr)

    assert res.status_code in (200, 400)
