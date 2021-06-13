#!/usr/bin/python3

import sys

import getopt
import json

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
	
	if ret != 0:
		sys.exit(1)
	
	if output == None :
		fp = sys.stdout
	else :
		fp = open(output, mode='w', encoding='utf-8')
	
	for filepath in args:
		data = read_json(filepath)
		for key in data :
			fp.write("{0}\n".format(key))
			for k in data[key] :
				fp.write("  {0}\n".format(k))
	
	if output == None :
		pass
	else :
		fp.close()

if __name__ == "__main__":
	main()
