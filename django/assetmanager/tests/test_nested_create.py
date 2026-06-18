import yaml
import requests
import urllib3
import pytest

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@pytest.mark.order(3)
def test_device_nested_create(configs):
    base_url = configs["base_url"]

    # nested_sample.yaml を読み込む
    with open("data/nested_sample.yaml") as fp:
        payload = yaml.safe_load(fp)

    # runserver_plus の /api/devices/ に POST
    response = requests.post(
        f"{base_url}/api/devices/",
        json=payload,
        verify=True,   # runserver_plus の自己署名証明書を無視
    )

    print("STATUS:", response.status_code)
    print("DATA:", response.json())

    # 201 Created を期待
    assert response.status_code == 201

    # 念のため、返ってきたデバイスの内容を軽くチェック
    created = response.json()
    assert "id" in created
    assert created["device_id"] == payload["device_id"]

