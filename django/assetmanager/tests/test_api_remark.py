# tests/test_api_remark.py

import pytest
import requests


@pytest.mark.order(30)
def test_remark_minimal(configs):
    url = f"{configs['base_url']}/api/remarks/"
    res = requests.get(url)
    assert res.status_code == 200

    remarks = res.json()
    assert isinstance(remarks, list)
    assert len(remarks) > 0

    r = remarks[0]
    assert "remark_id" in r
    assert "text" in r
    assert "device" in r


@pytest.mark.order(31)
def test_remark_get_detail(configs):
    # まず一覧を取得
    url = f"{configs['base_url']}/api/remarks/"
    res = requests.get(url)
    assert res.status_code == 200
    remarks = res.json()
    assert len(remarks) > 0

    rid = remarks[0]["id"]

    # 詳細取得
    url = f"{configs['base_url']}/api/remarks/{rid}/"
    res = requests.get(url)
    assert res.status_code == 200

    r = res.json()
    assert r["id"] == rid
    assert "remark_id" in r
    assert "text" in r
    assert "device" in r


@pytest.mark.order(32)
def test_remark_patch_text(configs):
    # 一覧取得
    url = f"{configs['base_url']}/api/remarks/"
    res = requests.get(url)
    assert res.status_code == 200
    remarks = res.json()
    assert len(remarks) > 0

    rid = remarks[0]["id"]

    # PATCH
    patch_url = f"{configs['base_url']}/api/remarks/{rid}/"
    payload = {"text": "UPDATED-REMARK"}
    res = requests.patch(patch_url, json=payload)
    assert res.status_code == 200

    # 再取得して確認
    res = requests.get(patch_url)
    assert res.status_code == 200
    r = res.json()
    assert r["text"] == "UPDATED-REMARK"


@pytest.mark.order(33)
def test_remark_delete(configs):
    # 一覧取得
    url = f"{configs['base_url']}/api/remarks/"
    res = requests.get(url)
    assert res.status_code == 200
    remarks = res.json()
    assert len(remarks) > 0

    rid = remarks[0]["id"]

    # DELETE
    del_url = f"{configs['base_url']}/api/remarks/{rid}/"
    res = requests.delete(del_url)
    assert res.status_code in (200, 204)

    # 再取得して 404 を確認
    res = requests.get(del_url)
    assert res.status_code == 404

