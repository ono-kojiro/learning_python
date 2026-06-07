import sys
import requests
import pytest

@pytest.mark.order(2)
def test_get_devices(configs):
    url = f"{configs['base_url']}/api/devices/"
    print(url, file=sys.stderr)

    res = requests.get(url)
    assert res.status_code == 200

    data = res.json()
    print(data, file=sys.stderr)

    # 最低1件は存在するはず（test_add_devicesで登録済み）
    assert isinstance(data, list)
    assert len(data) >= 1

    # デバイスの基本項目が存在するか確認
    first = data[0]
    assert "serial_number" in first
    assert "name" in first

