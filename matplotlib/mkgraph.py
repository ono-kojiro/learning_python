#!/usr/bin/python3

import sys

import getopt
import json

import re

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

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

	#fp.write("json test\n")
	fp.write("# rw	blocksize  bandwidth\n")

	last_rw = ''
	
	for input in args:
		#print("arg : {0}".format(input))
		fp_in = open(input, mode='r', encoding='utf-8')
		data = json.load(fp_in)
		fp_in.close()

		rw = data['global options']['rw']
		bs = data['global options']['bs']
		#print(rw)
		#print(bs)
		m = re.search(r'(\d+)k', bs)
		if m :
			bs = int(m.group(1)) * 1000
		else :
			print('invalid block size, {0}'.format(bs))
			sys.exit(1)

		if last_rw != '' and last_rw != rw :
			fp.write('\n')

		for job in data['jobs'] :
			name = job['jobname']
			bw = job[rw]['bw']

			fp.write('{0}\t{1}\t{2}\n'.format(rw, bs, bw))

		last_rw = rw		
		'''
		print(
			json.dumps(
				data,
			indent=4,
				ensure_ascii=False
			)
		)
		'''
	
	fp.close()
	
if __name__ == "__main__":
	main()
