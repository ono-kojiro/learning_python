#!/usr/bin/python3
# coding: utf-8

import sys
import re

import getopt
import codecs

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def main():
	ret = 0
	
	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvo:",
			[
				"help",
				"version",
				"output="]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = None
	
	for o, a in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-o", "--output"):
			output = a
		else:
			assert False, "unknown option"
	
	ret = 0
	
	if ret != 0:
		sys.exit(1)
	
	if output == None :
		fp_out = sys.stdout
	else :
		fp_out = codecs.open(output, "w", 'utf-8')

	num_json = 0

	for filepath in args:
		fp_in = codecs.open(filepath, "r", 'utf-8')
		state = 0
		lines = ''

		while 1:
			line = fp_in.readline()
			if not line:
				break
			
			line = line.rstrip()
			
			if re.search(r'^{\s*$', line) :
				state = 1
				print('start')
				lines = ''

			if state == 1 :
				lines += line + '\n'

			if re.search(r'^}\s*$', line) :
				print('end')
				state = 0
				fp_out.write(lines)
				num_json += 1
				lines = ''
		fp_in.close()
		
	if output == None :
		pass
	else :
		fp_out.close()

	print('num json : {0}'.format(num_json))

if __name__ == "__main__":
	main()
