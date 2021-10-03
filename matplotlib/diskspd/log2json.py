#!/usr/bin/python3

import sys

import getopt
import json

import re
	
STATE_INIT        = 0
STATE_COMMANDLINE = 1
STATE_SYSTEMINFO  = 2
STATE_INPUT_PARAM = 3
STATE_RESULT      = 4


def usage():
	print("Usage : {0}".format(sys.argv[0]))

def normalize_bs(bs_str) :
	m = re.search(r'(\d+(\.\d+)?)(K|M|G|Ki|Mi|Gi)?B', bs_str)
	if m :
		val = m.group(1)
		unit = m.group(3)
		if unit == 'K' :
			bs = int(float(val) * 1000) # for simplify
		elif unit == 'Ki' :
			bs = int(float(val) * 1024)
		elif unit == 'M' :
			bs = int(float(val) * 1000 * 1000) # for simplify
		elif unit == 'Mi' :
			bs = int(float(val) * 1024 * 1024)
		elif unit == 'G' :
			bs = int(float(val) * 1000 * 1000 * 1000) # for simplify
		elif unit == 'Gi' :
			bs = int(float(val) * 1024 * 1024 * 1024)
		else :
			bs = int(float(val))
	else :
		print('can not normalize blocksize, "{0}"'.format(bs_str))
		sys.exit(1)

	return bs

def normalize_bw(bw_str) :
	m = re.search(r'(\d+(\.\d+)?)\s*( |K|M|G|Ki|Mi|Gi)?B/s', bw_str)
	if m :
		val  = m.group(1)
		unit = m.group(3)
		if unit == 'K' :
			bw = int(float(val) * 1000)
		elif unit == 'Ki' :
			bw = int(float(val) * 1024)
		elif unit == 'M' :
			bw = int(float(val) * 1000 * 1000)
		elif unit == 'Mi' :
			bw = int(float(val) * 1024 * 1024)
		elif unit == 'G' :
			bw = int(float(val) * 1000 * 1000 * 1000)
		elif unit == 'Gi' :
			bw = int(float(val) * 1024 * 1024 * 1024)
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

def search_blocksize(line) :
    bs = ''
    m = re.search(r' bs=(\d+\w+)', line)
    if m :
        bs = m.group(1)
        bs = normalize_bs(bs)
 
    m = re.search(r'rw=(\w+), bs=\(R\) (\d+(\.\d+)?\w+)-(\d+(\.\d+)?\w+), \(W\) (\d+(\.\d+)?\w+)-(\d+(\.\d+)?\w+),', line)
    if m :
        rw = m.group(1)
        bs_r = m.group(2)
        bs_w = m.group(6)
        if re.search(r'read', rw) :
            bs = normalize_bs(bs_r)
        else :
            bs = normalize_bs(bs_w)
    return bs

def change_state(line, userdata) :
	ret = 0
	state = userdata['state']

	if state == STATE_INIT :
		if re.search(r'^Command Line:', line) :
			state = STATE_COMMANDLINE
	elif state == STATE_COMMANDLINE :
		if re.search(r'^System info:', line) :
			state = STATE_SYSTEMINFO
	elif state == STATE_SYSTEMINFO :
		if re.search(r'^Input parameters:', line) :
			state = STATE_INPUT_PARAM
	elif state == STATE_INPUT_PARAM :
		if re.search(r'^Results for job \d+:', line) :
			state = STATE_RESULT
	elif state == STATE_RESULT :
		pass

	userdata['state'] = state
	return ret

def procedure(line, userdata) :
	ret = 0
	state = userdata['state']

	if state == STATE_INIT :
		pass
	elif state == STATE_COMMANDLINE :
		pass
	elif state == STATE_SYSTEMINFO :
		pass
	elif state == STATE_INPUT_PARAM :
		m = re.search(r'\s+duration: (.+)s', line)
		if m :
			userdata['duration'] = m.group(1)
		
		m = re.search(r'\s+warm up time: (.+)s', line)
		if m :
			userdata['warm_up_time'] = m.group(1)
		
		m = re.search(r'\s+block size: (.+)', line)
		if m :
			userdata['block_size'] = m.group(1)
		
		m = re.search(r'\s+size: (.+)B$', line)
		if m :
			userdata['size'] = m.group(1)

	elif state == STATE_RESULT :
		#m = re.search(r'^Results for job (\d+):', line)
		#if m :
		#	userdata['_job_id'] = m.group(1)

		m = re.search(r'^(Total|Read|Write) IO$', line)
		if m :
			userdata['io_type'] = m.group(1)

		regex = r'^total:\s*(\d+) \|\s*(\d+) \|\s*(\d+(\.\d+)?) \|\s*(\d+(\.\d+)?)'
		m = re.search(regex, line)
		if m :
			num_bytes = m.group(1)
			num_ios   = m.group(2)
			bw        = m.group(3)
			iops      = m.group(5)

			io_type = userdata['io_type']

			result = {
				'io_type'   : io_type,
				'num_bytes' : num_bytes,
				'num_ios'      : num_ios,
				'bw'        : bw,
				'iops'      : iops
			}

			if io_type != 'Total' :
				userdata['results'].append(result)

	return ret

def postproc(line, userdata) :
	ret = 0
	state = userdata['state']

	if state == STATE_INIT :
		pass
	elif state == STATE_COMMANDLINE :
		pass
	elif state == STATE_SYSTEMINFO :
		pass
	elif state == STATE_INPUT_PARAM :
		pass
	elif state == STATE_RESULT :
		pass

	return ret

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

	data = []

	for filepath in args:
		fp_in = open(filepath, mode='r', encoding='utf-8')
	
		userdata = {
			"state" : STATE_INIT,
			"results" : [],
		}
		
		while 1:
			line = fp_in.readline()
			if not line :
				break

			line = re.sub(r'\r?\n?$', '', line)

			change_state(line, userdata)
			procedure(line, userdata)
			postproc(line, userdata)

		fp_in.close()

		data.append(userdata)

	for userdata in data:
		# remove internal variables
		userdata.pop('state', None)	
		userdata.pop('io_type', None)	

	fp_out.write(
		json.dumps(
			data,
			indent=2,
			sort_keys = True,
		)
	)

	if output != None :
		fp_out.close()
	
if __name__ == "__main__":
	main()
