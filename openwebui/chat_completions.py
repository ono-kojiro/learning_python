#!/usr/bin/env python3

import sys
import os

import re
import json

import getopt

import tomllib
from openwebui import Client

from pprint import pprint

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

    for filepath in args:
        params = {}

        configfiles = [
            './api_key.shrc',
            './config.shrc',
            filepath,
        ]
        for configfile in configfiles:
            with open(configfile, mode='rb') as f:
                params = params | tomllib.load(f)
        
        base_url = params['base_url']
        api_key  = params['api_key']

        model = params['model']
        collection = params['collection']
        query = params['query']

        client = Client(base_url, api_key)

        res = client.chat_completions(model, collection, query)
        pprint(res)
    
    if output is not None :
        fp.close()

if __name__ == "__main__" :
    main()

