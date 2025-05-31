#!/usr/bin/env python3

import sys
import os

import re
import json

import tomllib
from openwebui import Client

from pprint import pprint

def main():
    params = {}

    configs = [ './api_key.shrc', './config.shrc' ]
    for filepath in configs:
        with open(filepath, mode='rb') as f:
            params = params | tomllib.load(f)

    base_url = params['base_url']
    api_key  = params['api_key']

    client = Client(base_url, api_key)

    items = client.get_knowledges()
    for item in items:
        print('{0}, {1}'.format(item['name'], item['id']))
        print('  files: {0}'.format(item['files']))

if __name__ == "__main__" :
    main()

