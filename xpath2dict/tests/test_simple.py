#!/usr/bin/env python3

import sys
import os
import pytest

import json

from xpath2dict import xpath2dict

from pprint import pprint

def test_simple():
    res = 1
    data = {}
    xpath = '/path/to/name'
    value = '3'

    xpath2dict(data, xpath, value)
    got = "\n" + json.dumps(data, indent=2, sort_keys=True) + "\n"
    pprint(got)
    print(got, file=sys.stderr)
    exp = '''
{
  "path": {
    "to": {
      "name": 3
    }
  }
}
'''

    assert exp == got

