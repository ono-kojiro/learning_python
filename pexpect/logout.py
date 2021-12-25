#!/usr/bin/python3

import sys
import re

import getopt

import pexpect

from pprint import pprint

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvo:b:d:",
			[
				"help",
				"version",
				"output=",
				"baudrate=",
				"device=",
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = None
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
		elif opt in ("-b", "--baudrate"):
			baudrate = int(arg)
		elif opt in ("-d", "--device"):
			device = arg
	
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

	p = pexpect.spawnu('picocom -b {0} {1}'.format(baudrate, device))
	p.logfile = sys.stdout

	p.expect('Terminal ready')

	p.sendline('')
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
	
			if index == 0:
				break
			elif index == 1:
				p.sendline('root')
			elif index == 2:
				p.sendline('exit')

		except pexpect.EOF as e:
			print('ERROR : {0}'.format(e.message))
			break
		except pexpect.TIMEOUT :
			print('ERROR : {0}'.format(e.message))
			break

	if output is not None :
		fp.close()

if __name__ == "__main__":
	main()
