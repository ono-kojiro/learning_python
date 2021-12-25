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
	if filepath != '-' :
		fp = open(filepath, mode='r', encoding='utf-8')
	else :
		fp = sys.stdin

	lines = ''
	while 1 :
		line = fp.readline()
		if not line :
			break
		lines = lines + line

	if filepath != '-' :
		fp.close()

	return lines

def wait_prompt(p) :
	ret = 0

	try :
		index = p.expect(
			[
				r'\n(.*)# ',
			],
			timeout=5
		)

	except pexpect.EOF :
		print('EOF found', flush=True)
		ret = 1
	except pexpect.TIMEOUT :
		print('TIMEOUT occured', flush=True)
		ret = 1
	
	return ret


def check_exit_code(p) :
	ret = -1

	p.sendline('echo $?')
	while True :
		try :
			index = p.expect(
				[
					r'\n(.*)# ',
					r'\n(\d+)',
				],
				timeout=5
			)

			if index == 0 :
				break
			elif index == 1 :
				ret = int(p.after)
		except pexpect.EOF :
			print('EOF found', flush=True)
			break

		except pexpect.TIMEOUT :
			print('TIMEOUT occured', flush=True)
			break

	return ret

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
	configfile = None
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
		configfile = './config.json'
	
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

	p = pexpect.spawnu(
		'picocom -b {0} {1}'.format(baudrate, device),
		echo=False
	)

	p.setecho(False)
	p.logfile = None

	p.expect('Terminal ready')
	p.logfile = None
	p.logfile_send = sys.stdout
	p.logfile_read = None

	for filepath in args :
		lines = read_shell(filepath)
	
		lines = shlex.quote(lines)
		cmd = "sh -c " + lines

		p.logfile = None
		p.logfile_send = sys.stdout
		p.logfile_read = sys.stdout
		p.sendline(cmd)
		#p.logfile = sys.stdout
		ret = wait_prompt(p)

		ret = check_exit_code(p)
		if ret != 0 :
			print('\nERROR : exit code is NOT zero, {0}'.format(ret))
			break

	if output is not None :
		fp.close()

if __name__ == "__main__":
	main()
