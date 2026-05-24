import sys
import requests
import pytest

import yaml


@pytest.mark.order(1)
def test_add_devices(configs):
    items = yaml.safe_load(open('devices.yml'))

    for item in items:
        url = '{0}/api/device/add/'.format(configs['base_url'])
        json = item
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)
        res = requests.post(url, json=item)
        assert res.status_code == 200

@pytest.mark.order(2)
def test_add_netifs(configs):
    items = yaml.safe_load(open('netifs.yml'))

    for item in items:
        url = '{0}/api/netif/add/'.format(configs['base_url'])
        json = item
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)
        res = requests.post(url, json=item)
        assert res.status_code == 200

@pytest.mark.order(3)
def test_add_macaddress(configs):
    items = yaml.safe_load(open('macaddress.yml'))

    for item in items:
        url = '{0}/api/macaddress/add/'.format(configs['base_url'])
        json = item
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)
        res = requests.post(url, json=item)
        assert res.status_code == 200

@pytest.mark.order(4)
def test_add_ipaddress(configs):
    items = yaml.safe_load(open('ipaddress.yml'))

    for item in items:
        url = '{0}/api/ipaddress/add/'.format(configs['base_url'])
        json = item
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)
        res = requests.post(url, json=item)
        assert res.status_code == 200

@pytest.mark.order(10)
def test_list_ipaddress(configs, load_json, save_json):
    url = '{0}/api/ipaddress/1/'.format(configs['base_url'])
    res = requests.get(url)
    assert res.status_code == 200

    got = res.json()
    save_json("ipaddess.json", got)


