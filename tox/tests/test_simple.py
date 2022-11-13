#!/usr/bin/env python3
import mymodule

def test_simple():
    ret = mymodule.hello()
    assert ret == 3
