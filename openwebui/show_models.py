#!/usr/bin/env python3

import sys
import os

import re
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def read_params(filepath, params):
    fp = open(filepath, mode='r', encoding='utf-8')
    while True:
        line = fp.readline()
        if not line:
            break

        line = re.sub('\r?\n?$', '', line)
        m = re.search(r'(.+)\s*=\s*(.+)', line)
        if m :
            k = m.group(1)
            v = m.group(2)
            v = re.sub(r'^"', '', v)
            v = re.sub(r'"$', '', v)
            params[k] = v
    fp.close()

def main():
    params = {}

    read_params('./api_key.shrc', params)
    read_params('./config.shrc', params)
    #print(params)

    url = params['base_url'] + '/api/models'
    headers = {
        'Authorization': 'Bearer {0}'.format(params['api_key']),
    }

    res = requests.get(
        url,
        headers=headers,
        verify=False,
        )
    #print(res)
    data = json.loads(res.text)

    #print(
    #    json.dumps(
    #        data,
    #        indent=4,
    #        ensure_ascii=False,
    #    )
    #)

    for item in data['data']:
        print(item['name'])


if __name__ == "__main__" :
    main()

