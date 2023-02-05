#!/usr/bin/env python3

import sys
import os
import pytest

import json

import yaml
from yaml import SafeDumper

SafeDumper.add_representer(
    type(None),
    lambda dumper, value: dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
)

from xpath2dict import xpath2dict

from pprint import pprint

def test_basic_yaml():
    res = 1
    data = {}

    items = [
        [ '/path/to/name', 'myname' ],
        [ '/path/to/value', 'myvalue' ],
        [ '/path/to/sub/name', 'subname' ],
        [ '/path/to/sub/value', 'subvalue' ],
    ]

    for item in items :
        xpath = item[0]
        value = item[1]
        xpath2dict(data, xpath, value)

    got = "\n" + yaml.dump(data,
        Dumper=yaml.SafeDumper,
        indent=2,
        sort_keys=True,
        default_flow_style=False
    )

    #got = "\n" + json.dumps(data, indent=2, sort_keys=True) + "\n"
    pprint(got)
    print(got, file=sys.stderr)
    exp = '''
path:
  to:
    name: myname
    sub:
      name: subname
      value: subvalue
    value: myvalue
'''

    assert exp == got


def test_basic_json():
    res = 1
    data = {}

    items = [
        [ '/path/to/name', 'myname' ],
        [ '/path/to/value', 'myvalue' ],
        [ '/path/to/sub/name', 'subname' ],
        [ '/path/to/sub/value', 'subvalue' ],
    ]

    for item in items :
        xpath = item[0]
        value = item[1]
        xpath2dict(data, xpath, value)

    got = "\n" + json.dumps(data, indent=2, sort_keys=True) + "\n"
    pprint(got)
    print(got, file=sys.stderr)
    exp = '''
{
  "path": {
    "to": {
      "name": "myname",
      "sub": {
        "name": "subname",
        "value": "subvalue"
      },
      "value": "myvalue"
    }
  }
}
'''

    assert exp == got

