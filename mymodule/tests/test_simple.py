#!/usr/bin/env python3

import mymodule
from mymodule import hello

def test_module_function():
    ret = mymodule.hello()
    assert ret == 3

def test_simple():
    ret = hello()
    assert ret == 3


