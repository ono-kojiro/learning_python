#!/usr/bin/env python

from setuptools import setup
import unittest

def test_suite():
	loader = unittest.TestLoader()
	#return loader.discover('tests', pattern='test_*.py')
	return loader.discover('tests', pattern='test_*.sh')

setup(
	name='example',
	version='0.0.1',
    package_dir={"": "src"},
	py_modules=['example'],
	test_suite='setup.test_suite',
	tests_require=[
		'pytest',
	],
)

