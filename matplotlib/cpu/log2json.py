#!/usr/bin/python3

import sys

import getopt
import json

import re

def usage():
	print("Usage : {0}".format(sys.argv[0]))

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
	
	if output == None :
		print("no output option")
		ret += 1
	
	if ret != 0:
		sys.exit(1)

	fp = open(output, mode='w', encoding='utf-8')	

	records = []

	for filepath in args:
		fp_in = open(filepath, mode='r', encoding='utf-8')
		while 1:
			line = fp_in.readline()
			if not line:
				break

			line = re.sub(r'\r?\n?$', '', line)
			#print('DEBUG : {0}'.format(line))
			
			m = re.search(r'^Number of threads: (\d+)', line)
			if m :
				num_threads = m.group(1)
				continue
			m = re.search(r'events per second: (.+)', line)
			if m :
				eps = m.group(1)
				continue

		record = {
			"num_threads" : num_threads,
			"events_per_second" : eps,
		}
		records.append(record)


		fp_in.close()
	for record in records :
		num_threads = record['num_threads']
		eps = record['events_per_second']

		fp.write('{0}\t{1}\n'.format(num_threads, eps))

	fp.close()
	
if __name__ == "__main__":
	main()
