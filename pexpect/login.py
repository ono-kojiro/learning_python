#!/usr/bin/python3

import sys
import re

import getopt
import json

import pexpect

from pprint import pprint

def usage():
	print("Usage : {0}".format(sys.argv[0]))
        
def read_json(filepath) :
	fp = open(filepath, mode='r', encoding='utf-8')
	data = json.load(fp)
	fp.close()
	return data

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvo:c:",
			[
				"help",
				"version",
				"output=",
				"config=",
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = None
	configfile = None
	
	for opt, arg in opts:
		if opt == "-v":
			usage()
			sys.exit(0)
		elif opt in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif opt in ("-o", "--output"):
			output = arg
		elif opt in ("-c", "--config"):
			configfile = arg
	
	if configfile is None :
		print('no config option')
		ret += 1
	
	if ret != 0:
		sys.exit(1)
	
	if output is not None :
		fp = open(output, mode='w', encoding='utf-8')
	else :
		fp = sys.stdout

	config = read_json(configfile)
	password = config['password']

	baudrate = 115200
	device   = '/dev/ttyS0'

	fp.write('Hello World\n')
	p = pexpect.spawnu('picocom -b {0} {1}'.format(baudrate, device))
	
	p.expect('Terminal ready')
	print(p.before)
	print(p.after)

	p.sendline('\n')
	while True :
		try :
			index = p.expect(
				[
					'debian login:',
					'Password:',
					r'root@debian:.*# ',
				],
				timeout=5
			)
	
			print(p.before)
			print(p.after)

			if index == 0:
				print('INFO : login prompt found')
				p.sendline('root\n')
			elif index == 1:
				print('INFO : password prompt found')
				p.sendline('{0}\n'.format(password))
			elif index == 2:
				print('INFO : bash prompt found')
				break

		except pexpect.EOF :
			print('EOF found')
			break
		except pexpect.TIMEOUT :
			print('TIMEOUT occured')
			break

	if output is not None :
		fp.close()

if __name__ == "__main__":
	main()