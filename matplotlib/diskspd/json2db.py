#!/usr/bin/python3

import sys
import getopt
import json
import re
import sqlite3

from decimal import Decimal, ROUND_HALF_UP

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def create_table(conn, table):
	c = conn.cursor()

	sql = 'DROP TABLE IF EXISTS {0};'.format(table)
	c.execute(sql)

	sql = 'CREATE TABLE {0} ('.format(table)
	sql += 'id INTEGER PRIMARY KEY, '
	sql += 'env TEXT, '
	sql += 'tool TEXT, '
	sql += 'rw TEXT, '
	sql += 'bs_str TEXT, '
	sql += 'bs INTEGER, '
	sql += 'bw INTEGER'
	sql += ');'

	c.execute(sql)

def insert_record(conn, table, record):
	c = conn.cursor()
	sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ?, ?, ?, ? );'.format(table)
	list = [ 
		record['env'],
		record['tool'],
		record['rw'],
		record['bs_str'],
		record['bs'],
		record['bw']
	]

	c.execute(sql, list)

def normalize_duration(val_str) :
	val = None

	m = re.search(r'(\d+)(s)?', val_str)
	if m :
		val = m.group(1)
		unit = m.group(2)
		if unit == 's' :
			val = int(m.group(1))
		elif not unit :
			val = int(m.group(1))
		else :
			val = None
	
	if not val :
		print('invalid duration, {0}'.format(val_str))
		sys.exit(1)
	
	return val

def add_bs_unit(bs) :
	count = 0
	units = [ '', 'Ki', 'M', 'Gi' ]

	bs = int(bs)

	while bs % 1024 == 0 :
		count += 1
		bs = bs / 1024
	
	return str(int(bs)) + units[count]

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
	
	table = 'bw_table'
	conn = sqlite3.connect(output)
	
	create_table(conn, table)

	io_types = {
		"Read"  : "read",
		"Write" : "write",
	}

	for filepath in args:
		print('read {0}'.format(filepath))
		fp_in = open(filepath, mode='r', encoding='utf-8')
		data = json.load(fp_in)
		fp_in.close()

		env  = 'host'
		tool = 'diskspd'

		for job in data :
			bs = job['block_size']
			bs_str = add_bs_unit(bs)

			duration = int(job['duration'])

			for result in job['results'] :
				num_bytes = int(result['num_bytes'])
				bw = float(num_bytes) / float(duration)
				bw = Decimal(bw).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
				bw = int(bw)


				io_type = result['io_type']
				if io_type in io_types :
					rw = io_types[io_type]
				else :
					print('invalid io_type, {0}'.format(io_type))
					sys.exit(1)

				record = {
					'env'  : env,
					'tool' : tool,
					'rw'   : rw,
					'bs_str' : bs_str,
					'bs'   : bs,
					'bw'   : bw
				}

				if num_bytes != 0 :
					insert_record(conn, table, record)	

	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	main()
