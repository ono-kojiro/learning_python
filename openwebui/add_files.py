#!/usr/bin/env python3

import sys
import os

import getopt

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
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding='utf-8')
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    params = {}
    params = read_params('./api_key.shrc', params)
    params = read_params('./config.shrc', params)

    for filepath in args:
        url = params['base_url'] + '/api/v1/files/'
        headers = {
            'Authorization': 'Bearer {0}'.format(params['api_key']),
        }
        files = { 'file' : open(filepath, mode='rb') }

        res = requests.post(
            url,
            headers=headers,
            files=files,
            verify=False,
        )
        text = json.loads(res.text)
        pprint(text)
    
    if output is not None :
        fp.close()

if __name__ == "__main__" :
    main()

