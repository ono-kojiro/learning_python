#!/usr/bin/env python3

import os
import sys
import re

import getopt

import json
import xmltodict

from datetime import datetime
import dateutil.parser

from pprint import pprint

def usage():
	print("Usage : {0} [-o output.jsonl] [input.xml]".format(sys.argv[0]))

def xml2jsonl(fp, index, filepath) :
	count = 1
	fp_in = open(filepath, mode='r', encoding='utf-8')
	data = xmltodict.parse(fp_in.read())

	index_data = {
		"index" : {
			"_index" : index,
		}
	}

	if not 'testsuites' in data :
		print('no testsuites in {0}'.format(filepath))
		sys.exit(1)
	
	if not 'testsuite' in data['testsuites'] :
		print('no testsuite in {0}'.format(filepath))
		sys.exit(1)

	if isinstance(data['testsuites']['testsuite'], list) :
		testsuites = data['testsuites']['testsuite']
	elif 'testcase' in data['testsuites']['testsuite'] :
		testsuites = [ data['testsuites']['testsuite'] ]
	elif not 'testcase' in data['testsuites']['testsuite'] :
		print('no testcase in {0}'.format(filepath))
		sys.exit(1)

	for testsuite in testsuites :
		testcases = testsuite['testcase']
		for testcase in testcases :
			if not 'failure' in testcase :
				testcase['success'] = {
					'@message' : 'passed'
				}

			fp.write(
				json.dumps(
					index_data,
					ensure_ascii=False,
				)
			)
			fp.write('\n')
		
			fp.write(
				json.dumps(
					testcase,
					ensure_ascii=False,
				)
			)
			fp.write('\n')

			count += 1

	fp_in.close()

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvi:o:",
			[
				"help",
				"version",
				"index=",
				"output="
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = None
	index = None
	
	for o, a in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-i", "--index") :
			index = a
		elif o in ("-o", "--output"):
			output = a
		else:
			assert False, "unknown option"
	
	if index is None :
		print('ERROR : no index option')
		ret += 1

	if ret != 0:
		sys.exit(1)

	if len(args) == 0 :
		usage()
		sys.exit(1)
	
	if output is not None :
		fp = open(output, mode='w', encoding='utf-8')
	else :
		fp = sys.stdout

	for filepath in args:
		xml2jsonl(fp, index, filepath)
	
	if output is not None :
		fp.close()
	
if __name__ == "__main__":
	main()

