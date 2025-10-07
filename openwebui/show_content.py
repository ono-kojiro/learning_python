#!/usr/bin/env python3

import sys
import os

import re
import json
import getopt
import tomllib
import hashlib

from openwebui import Client

from pprint import pprint

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:a:c:",
            [
                "help",
                "version",
                "output=",
                "api-key=",
                "config=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    api_key_shrc = './api_key.shrc'
    config_shrc    = './config.shrc'

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-a", "--api-key"):
            api_key_shrc = a
        elif o in ("-c", "--config"):
            config_shrc = a
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding='utf-8')
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    params = {}

    configfiles = [ api_key_shrc, config_shrc ]
    for filepath in configfiles:
        with open(filepath, mode='rb') as f:
            params = params | tomllib.load(f)

    base_url = params['base_url']
    api_key  = params['api_key']

    client = Client(base_url, api_key)

    for filepath in args :
        filename = os.path.basename(filepath)
        item = client.get_file_by_name(filename)
        print(item)
        if not item :
            print('ERROR: no such filename, {0}'.format(filename))
            continue
        content = item['data']['content']
        #for line in content :
        #    print(line)

        algorithm = 'sha256'
        h = hashlib.new(algorithm)
        l = h.block_size * 0x800
        h.update(content.encode())
        print(h.hexdigest())

if __name__ == "__main__" :
    main()

