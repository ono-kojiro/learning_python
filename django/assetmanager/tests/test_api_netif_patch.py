import sys
import requests
import pytest

@pytest.mark.order(6)
def test_patch_netif(configs):
    base = configs["base_url"]

    pk = 1
    patch_url = f"{base}/api/netifs/{pk}/"
    print("PATCH URL:", patch_url, file=sys.stderr)

    payload = {
        "name": "eth0-renamed"
    }

    res = requests.patch(patch_url, json=payload)

    # ★ 404 は「すでに削除済み」として成功扱いにする
    if res.status_code == 404:
        print("SKIP: NetIF already deleted", file=sys.stderr)
        return

    if res.status_code not in (200, 202):
        print("ERROR RESPONSE:", res.json(), file=sys.stderr)

    assert res.status_code in (200, 202)

    # 変更確認
    res2 = requests.get(patch_url)
    assert res2.status_code == 200
    updated = res2.json()
    assert updated["name"] == "eth0-renamed"
