import sys
import requests
import pytest

@pytest.mark.order(2)
def test_get_devices(configs):
    url = f"{configs['base_url']}/api/devices/"
    res = requests.get(url)
    assert res.status_code == 200

    devices = res.json()
    assert len(devices) > 0

    device = devices[0]
    assert "id" in device

    # lookup_field = id に対応
    detail_url = f"{configs['base_url']}/api/devices/{device['id']}/"
    res2 = requests.get(detail_url)
    assert res2.status_code == 200
