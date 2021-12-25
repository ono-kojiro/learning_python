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
			"hvo:c:b:d:",
			[
				"help",
				"version",
				"output=",
				"config=",
				"baudrate=",
				"device=",
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = None
	configfile = 'config.json'
	baudrate = None
	device   = None
	
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
		elif opt in ("-b", "--baudrate"):
			baudrate = int(arg)
		elif opt in ("-d", "--device"):
			device = arg
	
	if configfile is None :
		print('no config option')
		ret += 1
	
	if baudrate is None :
		print('no baudrate option')
		ret += 1
	
	if device is None :
		print('no device option')
		ret += 1
	
	if ret != 0:
		sys.exit(1)
	
	if output is not None :
		fp = open(output, mode='w', encoding='utf-8')
	else :
		fp = sys.stdout

	config = read_json(configfile)
	password = config['password']

	try :
		p = pexpect.spawnu(
			'picocom -b {0} {1}'.format(baudrate, device),
			echo=False
		)
	
		p.logfile = sys.stderr

		p.expect(
			[
				'Terminal ready',
			]
		)
	
		p.sendline('')
	
		while True :
			index = p.expect(
				[
					'\ndebian login:',     # index 0
					'\nPassword:',         # index 1
					'\n(root@debian:.*)?# ', # index 2
				],
				timeout=5
			)
	
			if index == 0:
				p.logfile = None
				p.sendline('root')
				p.logfile = sys.stdout
			elif index == 1:
				p.logfile = None
				p.sendline('{0}'.format(password))
				p.logfile = sys.stdout
			elif index == 2:
				break

	except pexpect.EOF as e:
		print('EOF')
		sys.exit(1)
	except pexpect.TIMEOUT as e:
		print('TIMEOUT')
		sys.exit(1)
	except pexpect.ExceptionPexpect as e:
		print('ExceptionPexpect')
		sys.exit(1)

	if output is not None :
		fp.close()

if __name__ == "__main__":
	main()
