#!/usr/bin/env python3

import sys
import os

import re
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from pprint import pprint

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
    return params

def delete_file(params, file_id):
    url = params['base_url'] + '/api/v1/files/{0}'.format(file_id)
    headers = {
        'Authorization': 'Bearer {0}'.format(params['api_key']),
    }

    res = requests.delete(
        url,
        headers=headers,
        verify=False,
        )
    text = json.loads(res.text)

    print(
        json.dumps(
            text,
            indent=4,
            ensure_ascii=False,
        )
    )

def main():
    params = {}

    params = read_params('./api_key.shrc', params)
    params = read_params('./config.shrc', params)

    url = params['base_url'] + '/api/v1/files/'
    headers = {
        'Authorization': 'Bearer {0}'.format(params['api_key']),
    }

    res = requests.get(
        url,
        headers=headers,
        verify=False,
        )
    items = json.loads(res.text)

    for item in items:
        filename = item['filename']
        print('INFO: delete {0}'.format(filename))
        delete_file(params, item['id'])

if __name__ == "__main__" :
    main()

