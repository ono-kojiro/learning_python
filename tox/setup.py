from setuptools import setup
import unittest


def test_suite():
    return unittest.TestLoader().discover("tests", pattern="test_*.py")


setup(
    name="mymodule",
    version="0.0.1",
    py_modules=["mymodule"],
    test_suite="setup.test_suite",
)
