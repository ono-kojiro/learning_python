import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://localhost:8000"

def test_get_devices_from_runserver():
    # /api/devices/ に GET リクエスト
    response = requests.get(
        f"{BASE_URL}/api/devices/",
        verify=True,  # runserver_plus の自己署名証明書を無視
    )

    print("STATUS:", response.status_code)
    print("DATA:", response.json())

    # 正常に取得できているか確認
    assert response.status_code == 200

    # fixture がロードされていれば devices が 1 件以上あるはず
    devices = response.json()
    assert isinstance(devices, list)
    assert len(devices) > 0

def test_get_specific_device(configs):
    url = f"{configs['base_url']}/api/devices/1/"
    res = requests.get(url)
    print(res.status_code, res.json())
    assert res.status_code == 200

