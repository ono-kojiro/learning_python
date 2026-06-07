import sys
import requests
import pytest

@pytest.mark.order(6)
def test_patch_netif(configs):
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

    patch_url = f"{base}/api/netifs/{netif_id}/"
    print("PATCH URL:", patch_url, file=sys.stderr)

    payload = {
        "name": "eth0-renamed"
    }

    res = requests.patch(patch_url, json=payload)

    # 削除済みならスキップ
    if res.status_code == 404:
        print("SKIP: NetIF already deleted", file=sys.stderr)
        return

    assert res.status_code in (200, 202)

    # 変更確認
    res2 = requests.get(patch_url)
    assert res2.status_code == 200
    updated = res2.json()
    assert updated["name"] == "eth0-renamed"
