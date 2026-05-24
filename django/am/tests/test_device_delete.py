import sys
import requests
import pytest

import yaml

@pytest.mark.order(900)
def test_device_delete(configs):
    url = '{0}/api/device/1/'.format(configs['base_url'])
    res = requests.delete(url)
    assert res.status_code == 200

