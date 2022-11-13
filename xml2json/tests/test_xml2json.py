#!/usr/bin/env python3

import os
import pytest

import subprocess

script = '../_build/lib/xml2json.py'

def test_run_test01():
	res = 1
	xmlfile  = 'input01.xml'
	jsonfile = 'output01.json'

	res = subprocess.call(['python3', script,
		'-o', jsonfile,
		xmlfile ]
	)
	assert res == 0

def test_run_test02():
	res = 1
	xmlfile  = 'input02.xml'
	jsonfile = 'output02.json'

	res = subprocess.call(['python3', script,
		'-o', jsonfile,
		xmlfile ]
	)
	assert res == 0

def test_run_test03():
	res = 1
	xmlfile  = 'input03.xml'
	jsonfile = 'output03.json'

	res = subprocess.call(['python3', script,
		'-o', jsonfile,
		xmlfile ]
	)
	assert res == 0


