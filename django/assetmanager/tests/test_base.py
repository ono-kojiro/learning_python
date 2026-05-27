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

        params = { "serial_number": item["serial_number"] }
        res = requests.get("{0}".format(url), params=params)
        if res.status_code == 200 and len(res.json()) > 0:
            continue

        res = requests.post(url, json=item)
        assert res.status_code == 201

@pytest.mark.order(2)
def test_add_ipv4s(configs):
    items = yaml.safe_load(open('ipv4s.yml'))

    for item in items:
        url = '{0}/api/ipv4s/'.format(configs['base_url'])
        json = item
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)
        res = requests.get("{0}?ipv4_id={1}".format(url, item['ipv4_id']))
        if res.status_code == 200 and len(res.json()) > 0:
            continue
        res = requests.post(url, json=item)
        assert res.status_code == 201

@pytest.mark.order(3)
def test_add_netifs(configs):
    items = yaml.safe_load(open('netifs.yml'))

    for item in items:
        url = '{0}/api/netifs/'.format(configs['base_url'])
        json = item
        print(url, file=sys.stderr)
        print(item, file=sys.stderr)

        params = {
            "devicd": item["device"],
            "name":   item["name"],
        }
        res = requests.get("{0}".format(url), params=params)
        if res.status_code == 200 and len(res.json()) > 0:
            continue
        
        res = requests.post(url, json=item)
        assert res.status_code == 201

