import pytest

from mypackage.mymodule import myfunc, return_zero, return_one

def test_example():
    assert 1 +2 == 3
    myfunc()

def test_zero():
    assert return_zero() == 0

def test_one():
    assert return_one() == 1


