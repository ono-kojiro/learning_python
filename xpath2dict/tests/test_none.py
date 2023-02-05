#!/usr/bin/env python3

import sys
import os
import pytest

import json

from xpath2dict import xpath2dict

from pprint import pprint

def test_none():
    res = 1
    data = {}
    xpath2dict(data, "/path/to/var", None)

    got = "\n" + json.dumps(data, indent=2, sort_keys=True) + "\n"
    exp = '''
{
  "path": {
    "to": {
      "var": {}
    }
  }
}
'''
    pprint(got)
    pprint(exp)
    assert exp == got

