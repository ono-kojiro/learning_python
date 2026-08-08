#!/usr/bin/env python3

from opnsense.core.api.system import System

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import json

from dotenv import load_dotenv, dotenv_values

def main():
    config = dotenv_values(".env")

    key = config.get("key")
    secret = config.get("secret")

    base_url = "https://192.168.122.99"

    api_key = "{0}:{1}".format(key, secret)

    api = System(base_url, api_key=api_key)

    r = api.status()
    print(json.dumps(r.json()))

if __name__ == "__main__":
    main()

