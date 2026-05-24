import sys
import requests
import pytest

import yaml

@pytest.mark.order(100)
def test_device_tree(configs, load_json, save_json):
    url = '{0}/api/device/tree/'.format(configs['base_url'])
    res = requests.get(url)
    assert res.status_code == 200

    got = res.json()
    save_json("test_device_tree.json", got)

