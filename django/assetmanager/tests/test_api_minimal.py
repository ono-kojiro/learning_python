import sys
import requests
import pytest
import yaml

@pytest.mark.order(1)
def test_add_devices(configs):
    # 最小の devices.yml を読み込む
    items = yaml.safe_load(open('devices.yml'))

    for item in items:
        url = f"{configs['base_url']}/api/devices/"
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)

        # すでに存在するかチェック
        params = { "serial_number": item["serial_number"] }
        res = requests.get(url, params=params)

        if res.status_code == 200 and len(res.json()) > 0:
            # すでに登録済みならスキップ
            continue

        # 新規登録
        res = requests.post(url, json=item)
        assert res.status_code == 201

