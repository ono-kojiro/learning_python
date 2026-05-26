import sys
import requests
import pytest

import yaml


@pytest.mark.order(1)
def test_add_devices(configs):
    items = yaml.safe_load(open('devices.yml'))

    for item in items:
        url = '{0}/api/devices/'.format(configs['base_url'])
        json = item
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)
        res = requests.post(url, json=item)
        assert res.status_code == 201

