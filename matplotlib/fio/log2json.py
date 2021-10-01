#!/usr/bin/python3

import sys

import getopt
import json

import re

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def normalize_bs(bs_str) :
	m = re.search(r'(\d+)(B|KiB|MiB)', bs_str)
	if m :
		val = m.group(1)
		unit = m.group(2)
		if unit == 'KiB' :
			bs = int(int(val) * 1000) # for simplify
		elif unit == 'MiB' :
			bs = int(int(val) * 1000 * 1000) # for simplify
		else :
			bs = int(val)
	else :
		print('can not normalize blocksize, "{0}"'.format(bs_str))
		sys.exit(1)

	return bs

def normalize_bw(bw_str) :
	m = re.search(r'(\d+(\.\d+)?)\s*( |Ki|Mi|Gi)?B/s', bw_str)
	if m :
		val  = m.group(1)
		unit = m.group(3)
		if unit == 'Ki' :
			bw = int(float(val) * 1000)
		elif unit == 'Mi' :
			bw = int(float(val) * 1000 * 1000)
		elif unit == 'Gi' :
			bw = int(float(val) * 1000 * 1000 * 1000)
		else :
			bw = int(val)
	else :
		print('can not normalize bandwidth, "{0}"'.format(bw_str))
		sys.exit(1)

	return bw

def split_params(line) :
	results = {
		'bw' : 0,
	}
	m = re.search(r'(bw|aggrb)=(.+?B/s)', line, re.IGNORECASE)
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
		"global options" : {
			"rw" : ""	
		},
		"jobs" : []
	}


	for filepath in args:
		fp_in = open(filepath, mode='r', encoding='utf-8')
	
		rw = ''
		while 1:
			line = fp_in.readline()
			if not line :
				break

			line = re.sub(r'\r?\n?$', '', line)

			m = re.search(r' rw=(.+),', line)
			if m :
				rw = m.group(1)
				data['global options']['rw'] = rw

			m = re.search(r' bs=\(R\) (\d+\w+)-(\d+\w+), \(W\) (\d+\w+)-(\d+\w+),', line)
			if m :
				bs_r = m.group(1)
				bs_w = m.group(3)

				if re.search(r'read', rw) :
					bs = normalize_bs(bs_r)
				elif re.search(r'write', rw) :
					bs = normalize_bs(bs_w)
				else :
					print('invalid rw, "{0}"'.format(rw))
					sys.exit(1)
				data['global options']['bs'] = bs
			

			#m = re.search(r'^\s+(read|write)\s*:\s*(.+)', line, re.IGNORECASE)
			m = re.search(r'^\s+(read|write)\s*:\s*(.+)', line)
			if m :
				print('{0}'.format(line))
				rw = m.group(1)
				params = m.group(2)

				results = split_params(params)
				#print(results)
				bw = results['bw']
				print('normalize "{0}"'.format(bw))
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
