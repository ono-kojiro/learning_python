#!/usr/bin/env python3

import os
import pytest

import subprocess

script = '../_build/lib/xml2json.py'

def test_junit():
	res = 1
	xmlfile  = '../data/junit_report.xml'
	jsonfile = 'junit_report.json'

	res = subprocess.call(['python3', script,
		'-o', jsonfile,
		xmlfile ]
	)
	assert res == 0

