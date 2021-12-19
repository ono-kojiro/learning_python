#!/usr/bin/python3

import sys
import re

import getopt
import json

import pexpect
import shlex

from pprint import pprint

def usage():
	print("Usage : {0}".format(sys.argv[0]))
        
def read_json(filepath) :
	fp = open(filepath, mode='r', encoding='utf-8')
	data = json.load(fp)
	fp.close()
	return data

def read_shell(filepath) :
	fp = open(filepath, mode='r', encoding='utf-8')
	lines = ''
	while 1 :
		line = fp.readline()
		if not line :
			break
		lines = lines + line
	lines = shlex.quote(lines)

	fp.close()
	return lines

def wait_prompt(p) :
	try :
		index = p.expect(
			[
				r'root@debian:.*# ',
			],
			timeout=5
		)

	except pexpect.EOF :
		print('EOF found')
	except pexpect.TIMEOUT :
		print('TIMEOUT occured')


def check_exit_code(p) :
	ret = -1

	p.sendline('echo $?')
	while True :
		try :
			index = p.expect(
				[
					r'root@debian:.*# ',
					'\d+',
				],
				timeout=5
			)

			if index == 0 :
				break
			elif index == 1 :
				ret = int(p.after)
		except pexpect.EOF :
			print('EOF found')
		except pexpect.TIMEOUT :
			print('TIMEOUT occured')

	return ret

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
		configfile = './config.json'
	
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

	p = pexpect.spawnu('picocom -b {0} {1}'.format(baudrate, device))
	p.logfile = sys.stdout

	p.expect('Terminal ready')

	for filepath in args :
		lines = read_shell(filepath)
		cmd = "bash -s -c " + lines
		p.sendline(cmd)
		wait_prompt(p)

		ret = check_exit_code(p)
		print('')
		print('INFO : ret is {0}'.format(ret))

	if output is not None :
		fp.close()

if __name__ == "__main__":
	main()
