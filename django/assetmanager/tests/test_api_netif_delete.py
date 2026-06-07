import sys
import requests
import pytest

@pytest.mark.order(7)
def test_delete_netif(configs):
    base = configs["base_url"]

    # 一覧取得
    list_url = f"{base}/api/netifs/"
    res = requests.get(list_url)
    assert res.status_code == 200

    netifs = res.json()
    print("NETIFS:", netifs, file=sys.stderr)

    if len(netifs) == 0:
        print("SKIP: No NetIF exists", file=sys.stderr)
        return

    target = netifs[0]
    netif_id = target["netif_id"]

    delete_url = f"{base}/api/netifs/{netif_id}/"
    print("DELETE URL:", delete_url, file=sys.stderr)

    res = requests.delete(delete_url)

    # DELETE は冪等なので 404 も許容
    assert res.status_code in (200, 202, 204, 404)

    # 削除確認
    res2 = requests.get(delete_url)
    assert res2.status_code == 404
