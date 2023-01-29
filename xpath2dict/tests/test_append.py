#!/usr/bin/env python3

import sys
import os
import pytest

import json

from xpath2dict import xpath2dict

from pprint import pprint

def test_append():
    res = 1
    data = {}
    xpath2dict(data, "/path/to/var", 1)
    xpath2dict(data, "/path/to/var", 2)

    got = "\n" + json.dumps(data, indent=2, sort_keys=True) + "\n"
    exp = '''
{
  "path": {
    "to": {
      "var": [
        1,
        2
      ]
    }
  }
}
'''
    pprint(got)
    pprint(exp)
    assert exp == got

