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

    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]

    # NetIF が IPv4 を持たないモデルに合わせたチェック
    assert "id" in first
    assert "netif_id" in first
    assert "name" in first
    assert "device" in first

    # IPv4 は NetIF に含まれない
    assert "ipv4" not in first
