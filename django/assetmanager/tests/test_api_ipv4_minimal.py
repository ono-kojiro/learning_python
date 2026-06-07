import sys
import requests
import pytest
import yaml

@pytest.mark.order(3)
def test_add_ipv4s(configs):
    items = yaml.safe_load(open('ipv4s.yml'))

    for item in items:
        url = f"{configs['base_url']}/api/ipv4s/"
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)

        # すでに存在するかチェック
        params = { "address": item["address"] }
        res = requests.get(url, params=params)

        if res.status_code == 200 and len(res.json()) > 0:
            continue

        # 新規登録
        res = requests.post(url, json=item)

        if res.status_code != 201:
            print("ERROR RESPONSE:", res.json(), file=sys.stderr)

        assert res.status_code == 201
