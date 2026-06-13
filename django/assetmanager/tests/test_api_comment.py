import pytest
import requests
import sys


@pytest.mark.order(20)
def test_comment_minimal(configs):
    url = f"{configs['base_url']}/api/comments/"
    res = requests.get(url)
    assert res.status_code == 200

    comments = res.json()
    assert isinstance(comments, list)
    assert len(comments) > 0

    c = comments[0]
    assert "id" in c
    assert "text" in c
    assert "device" in c


@pytest.mark.order(21)
def test_get_comment(configs):
    # 一覧から id を取得
    url_list = f"{configs['base_url']}/api/comments/"
    res_list = requests.get(url_list)
    assert res_list.status_code == 200

    comments = res_list.json()
    assert len(comments) > 0

    id = comments[0]["id"]

    url = f"{configs['base_url']}/api/comments/{id}/"
    res = requests.get(url)
    assert res.status_code == 200

    data = res.json()
    assert data["id"] == id
    assert "text" in data
    assert "device" in data


@pytest.mark.order(22)
def test_patch_comment(configs):
    # 一覧から id を取得
    url_list = f"{configs['base_url']}/api/comments/"
    res_list = requests.get(url_list)
    assert res_list.status_code == 200

    comments = res_list.json()
    assert len(comments) > 0

    id = comments[0]["id"]

    url = f"{configs['base_url']}/api/comments/{id}/"

    payload = {
        "text": "Updated comment text"
    }

    res = requests.patch(url, json=payload)
    print("PATCH RESULT:", res.json(), file=sys.stderr)
    assert res.status_code == 200

    data = res.json()
    assert data["text"] == "Updated comment text"


@pytest.mark.order(23)
def test_delete_comment(configs):
    # 一覧から idを取得
    url_list = f"{configs['base_url']}/api/comments/"
    res_list = requests.get(url_list)
    assert res_list.status_code == 200

    comments = res_list.json()
    assert len(comments) > 0

    id = comments[0]["id"]

    url = f"{configs['base_url']}/api/comments/{id}/"

    res = requests.delete(url)
    assert res.status_code in (200, 204)

    # 削除確認
    res2 = requests.get(url)
    assert res2.status_code == 404

