#!/usr/bin/python3

import sys

import getopt
import json

import re

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def normalize_bw(bw_str) :
	m = re.search(r'(\d+(\.\d+)?)\s*( |K|M|G)B/s', bw_str)
	if m :
		val  = m.group(1)
		unit = m.group(3)
		if unit == 'K' :
			bw = int(float(val) * 1000)
		elif unit == 'M' :
			bw = int(float(val) * 1000 * 1000)
		elif unit == 'G' :
			bw = int(float(val) * 1000 * 1000 * 1000)
		else :
			bw = int(val)
	else :
		print('can not normalize bandwidth, "{0}"'.format(bw))
		sys.exit(1)

	return bw

def split_params(line) :
	results = {
		'bw' : 0,
	}
	m = re.search(r'(bw|aggrb)=(.+?B/s),', line)
	if m :
		results['bw'] = m.group(2)

	return results
		
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
		fp_out = sys.stdout
	else :
		fp_out = open(output, mode="w", encoding='utf-8')
		
	if ret != 0:
		sys.exit(1)
	

	data = {
		'jobs' : []
	}

	num_jobs = 0

	for filepath in args:
		fp_in = open(filepath, mode='r', encoding='utf-8')
		while 1:
			line = fp_in.readline()
			if not line :
				break

			line = re.sub(r'\r?\n?$', '', line)

			#m = re.search(r'^\s+(read|write)\s*:\s*(.+)', line, re.IGNORECASE)
			m = re.search(r'^\s+(read|write)\s*:\s*(.+)', line)
			if m :
				print('{0}'.format(line))
				rw = m.group(1)
				params = m.group(2)

				results = split_params(params)
				#print(results)
				bw = normalize_bw(results['bw'])
				#print('bw = {0}'.format(bw))

				item = {
					rw : {
						'bw' : bw
					}
				}

				data['jobs'].append(item)

		fp_in.close()

	fp_out.write(
		json.dumps(
			data,
#			indent=2,
			sort_keys = True,
		)
	)

	if output != None :
		fp_out.close()
	
if __name__ == "__main__":
	main()
