import sys
import requests
import pytest

@pytest.mark.order(7)
def test_delete_netif(configs):
    base = configs["base_url"]

    pk = 1
    delete_url = f"{base}/api/netifs/{pk}/"
    print("DELETE URL:", delete_url, file=sys.stderr)

    res = requests.delete(delete_url)

    # 404 でも「削除済み」として成功扱いにする
    assert res.status_code in (200, 202, 204, 404)

    # 削除確認（404 が正しい）
    res2 = requests.get(delete_url)
    assert res2.status_code == 404
