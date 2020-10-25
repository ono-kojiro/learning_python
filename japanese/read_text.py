#!/usr/bin/python
# coding: utf-8

import sys

import getopt
import codecs

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def main():
	print('sys.getdefaultencoding: ' + sys.getdefaultencoding())
	
	try:
		opts, args = getopt.getopt(
                    sys.argv[1:], "hvo:", ["help", "version", "output="])
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

	for input in args:
		fp_in = codecs.open(input, "r", 'utf-8')
		while 1:
			line = fp_in.readline()
			line = line.rstrip()
			if not line:
				break
			
			# ファイルに書き出すときはdecodeしない
			fp_out.write(line + '\n')
			
			# printのときはutf-8にdecodeする必要がある
			#print("PRINT : {0}".format(line.encode('cp932')))
			print("PRINT : {0}".format(line))
		fp_in.close()
		
	fp_out.close()

if __name__ == "__main__":
	main()
