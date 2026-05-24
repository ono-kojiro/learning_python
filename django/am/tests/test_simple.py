import sys
import requests
import pytest

import yaml

@pytest.mark.order(1)
def test_simple(configs):
    url = '{0}/'.format(configs['base_url'])
    res = requests.get(url)
    assert res.status_code == 200

