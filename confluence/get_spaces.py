#!/usr/bin/python3

import sys
import os

import getopt
import json
import re

#from atlassian import Jira
from atlassian import Confluence

from pprint import pprint

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def read_netrc() :
	home = os.getenv('HOME')
	filepath = '{0}/.netrc'.format(home)
	fp = open(filepath, mode='r', encoding='utf-8')

	userinfo = {}
	record = {}
	while 1:
		line = fp.readline()
		if not line :
			break

		for m in re.finditer(r'(machine|login|password)\s+([^\s]+)', line) :
			key = m.group(1)
			val = m.group(2)
			record[key] = val

			if 'machine' in record \
				and 'login' in record \
				and 'password' in record :

				machine  = record['machine']
				login    = record['login']
				password = record['password']
				userinfo[machine] = {
					'login' : login,
					'password' : password,
				}
				record = {}

	fp.close()

	return userinfo

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hv",
			[
				"help",
				"version",
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)

	for o, optarg in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		else:
			assert False, "unknown option"
	
	if ret != 0:
		sys.exit(1)
	
	userinfo = read_netrc()

	for url in args :
		username = ''
		password = ''

		for machine in userinfo :
			if machine in url :
				username = userinfo[machine]['login']
				password = userinfo[machine]['password']

		if username == '' or password == '' :
			print('no username/password for {0}'.format(url))
			sys.exit(1)

		confluence = Confluence(
			url=url,
			username=username,
			password=password
		)

		spaces = confluence.get_all_spaces(start=0, limit=500, expand=None)
		if 'results' in spaces :
			for result in spaces['results'] :
				name = result['name']
				print(name)
	
if __name__ == "__main__":
	main()
