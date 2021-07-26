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

def get_child_pages(confluence, parent_id, title) :
	pages = confluence.get_page_child_by_type(parent_id, type='page', start=None, limit=None)

	for page in pages :
		page_id    = page['id']
		page_title = page['title']

		if page_title == title:
			yield page_id

		for sub_page_id in get_child_pages(confluence, page_id, title) :
			yield sub_page_id

def read_data(datafile) :
	fp = open(datafile, mode='r', encoding='utf-8')
	lines = ''
	while 1:
		line = fp.readline()
		if not line :
			break
		lines += line

	fp.close()
	return lines

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvs:p:t:d:",
			[
				"help",
				"version",
				"space=",
				"parent=",
				"title=",
				"data=",
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)

	space  = None
	parent = None
	title  = None
	data   = None
	
	for o, optarg in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-s", "--space"):
			space = optarg
		elif o in ("-p", "--parent"):
			parent = optarg
		elif o in ("-t", "--title"):
			title = optarg
		elif o in ("-d", "--data"):
			data = optarg
		else:
			assert False, "unknown option"
	
	if space == None :
		print("no space option")
		ret += 1
	if parent == None :
		print("no parent option")
		ret += 1
	if title == None :
		print("no title option")
		ret += 1
	if data == None :
		print("no data option")
		ret += 1
	
	if ret != 0:
		sys.exit(1)
	
	userinfo = read_netrc()

	if re.search(r'^@', data) :
		datafile = re.sub(r'^@', '', data)
		data = read_data(datafile)
	else :
		print('data is ' + data)

	body = data

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

		parent_id = confluence.get_page_id(space, parent)
		#print('{0}:{1}'.format(parent_id, parent))

		for page_id in get_child_pages(confluence, parent_id, title) :
			print('update page {0} ({1})'.format(title, page_id))
			confluence.update_page(page_id, title, body, parent_id, 'page', 'storage', False)
	
if __name__ == "__main__":
	main()
