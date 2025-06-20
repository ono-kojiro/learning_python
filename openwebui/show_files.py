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

    url = base_url + '/api/v1/files/'
    headers = {
        'Authorization': 'Bearer {0}'.format(api_key),
    }

    client = Client(base_url, api_key)
    client.show_files()

if __name__ == "__main__" :
    main()

