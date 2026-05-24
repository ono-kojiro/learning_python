import sys
import requests
import pytest

import yaml

@pytest.mark.order(100)
def test_device_tree(configs):
    url = '{0}/api/device/tree/'.format(configs['base_url'])
    res = requests.get(url)
    assert res.status_code == 200

