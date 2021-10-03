#!/usr/bin/python3

import sys

import getopt
import json

import re
import sqlite3

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def normalize_bs(bs_str) :
	m = re.search(r'(\d+(\.\d+)?)(K|M|G|Ki|Mi|Gi)?(B)?', bs_str)
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
	fp.write('# env, tool, rw, bs_str, bs, bw\n')
	for database in args:
		table = 'bw_table'
		conn = sqlite3.connect(database)
		conn.row_factory = sqlite3.Row

		sql = 'SELECT env, tool, rw, bs_str, bs, bw FROM {0}'.format(table)
		sql += ' ORDER BY env ASC, tool ASC, rw ASC, bs ASC;'

		c = conn.cursor()
		rows = c.execute(sql)

		last_rw   = ''

		for row in rows :
			env  = row['env']
			tool = row['tool']
			rw   = row['rw']
			bs_str = row['bs_str']
			bs   = int(row['bs'])
			bw   = int(row['bw'])

			#bs = normalize_bs(bs)

			if last_rw != '' and last_rw != rw :
				fp.write('\n')
			fp.write('{0}\t{1}\t{2}\t{3:6}\t{4}\t{5}\n'.format(
				env, tool, rw, bs_str, bs, bw))

			last_rw = rw

		conn.close()

	fp.close()

if __name__ == "__main__":
	main()
