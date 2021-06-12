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
	
	if output == None :
		print("no output option")
		ret += 1
	
	if ret != 0:
		sys.exit(1)
	
	fp_out = codecs.open(output, "w", 'utf-8')

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
				lines = ''
		fp_in.close()
		
	fp_out.close()

if __name__ == "__main__":
	main()
