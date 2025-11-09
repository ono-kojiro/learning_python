#/usr/bin/env python3

import sys
import os

import getopt

import re
import json

import tomllib
from OpenWebUI import Client

import json
from pprint import pprint

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:a:c:m:q:",
            [
                "help",
                "version",
                "output=",
                "api-key=",
                "config=",
                "model=",
                "query=",
                "collection=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None

    model      = None
    query      = None
    collection = None

    api_key_shrc = './api_key.shrc'
    config_shrc  = './config.shrc'

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("--api-key"):
            api_key_shrc = a
        elif o in ("--config"):
            config_shrc = a
        elif o in ("-m", "--model"):
            model = a
        elif o in ("-q", "--query"):
            query = a
        elif o in ("-c", "--collection"):
            collection = a
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout

    if model is None:
        print('ERROR: no model option')
        ret += 1
    
    if query is None:
        print('ERROR: no query option')
        ret += 1
    
    if collection is None:
        print('ERROR: no collection option')
        ret += 1

    if ret :
        sys.exit(ret)

    configs = [ api_key_shrc, config_shrc ]
    
    params = {}
    for filepath in configs:
        with open(filepath, mode='rb') as f:
            params = params | tomllib.load(f)

    base_url = params['base_url']
    api_key  = params['api_key']

    client = Client(base_url, api_key)

    res = client.chat_completions_async(model, query, collection)
    #res = client.chat_completions(model, query, collection)

    if output is not None :
        fp.close()

if __name__ == "__main__" :
    main()

