#!/usr/bin/env python3

import os
import pytest

import subprocess

xml2json  = '../_build/lib/xml2json.py'
xml2jsonl = '../_build/lib/xml2jsonl.py'

def test_junit_json():
	res = 1
	xmlfile  = '../data/junit_report.xml'
	jsonfile = 'junit_report.json'

	res = subprocess.call(['python3', xml2json,
		'-o', jsonfile,
		xmlfile ]
	)
	assert res == 0

def test_junit_jsonl():
	res = 1
	xmlfile  = '../data/junit_report.xml'
	jsonfile = 'junit_report.jsonl'
	index    = 'myindex'

	res = subprocess.call(['python3', xml2jsonl,
        '-i', index,
		'-o', jsonfile,
		xmlfile ]
	)
	assert res == 0

