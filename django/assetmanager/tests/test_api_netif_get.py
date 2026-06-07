import sys
import requests
import pytest

@pytest.mark.order(5)
def test_get_netifs(configs):
    url = f"{configs['base_url']}/api/netifs/"
    print(url, file=sys.stderr)

    res = requests.get(url)
    assert res.status_code == 200

    data = res.json()
    print("NETIFS:", data, file=sys.stderr)

    # 最低1件は存在するはず（test_add_netifs で登録済み）
    assert isinstance(data, list)
    assert len(data) >= 1

    first = data[0]
    assert "name" in first
    assert "netif_id" in first
    assert "device" in first
    assert "ipv4" in first

