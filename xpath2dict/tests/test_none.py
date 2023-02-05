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

def test_none_yaml():
    res = 1
    data = {}
    xpath2dict(data, "/path/to/var", None)

    #got = "\n" + json.dumps(data, indent=2, sort_keys=True) + "\n"
    got = "\n" + yaml.dump(data,
            Dumper=yaml.SafeDumper,
            indent=2,
            sort_keys=True,
            default_flow_style=False
        )
  
    exp = '''
path:
  to:
    var:
'''
    pprint(got)
    pprint(exp)
    assert exp == got


def test_none_json():
    res = 1
    data = {}
    xpath2dict(data, "/path/to/var", None)

    got = "\n" + json.dumps(data, indent=2, sort_keys=True) + "\n"
    exp = '''
{
  "path": {
    "to": {
      "var": null
    }
  }
}
'''
    pprint(got)
    pprint(exp)
    assert exp == got

