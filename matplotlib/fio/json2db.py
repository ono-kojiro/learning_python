#!/usr/bin/python3

import sys
import getopt
import json
import re
import sqlite3

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def create_table(conn, table):
	c = conn.cursor()

	sql = 'DROP TABLE IF EXISTS {0};'.format(table)
	c.execute(sql)

	sql = 'CREATE TABLE {0} ('.format(table)
	sql += 'id INTEGER PRIMARY KEY, '
	sql += 'name TEXT, '
	sql += 'env TEXT, '
	sql += 'fmt TEXT, '
	sql += 'rw TEXT, '
	sql += 'bs INTEGER, '
	sql += 'bw INTEGER '
	sql += ');'

	c.execute(sql)

def insert_record(conn, table, record):
	c = conn.cursor()
	sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ?, ?, ?, ? );'.format(table)
	list = [ 
		record['name'],
		record['env'],
		record['fmt'],
		record['rw'],
		record['bs'],
		record['bw']
	]

	c.execute(sql, list)

def normalize_blocksize(bs_str) :
	m = re.search(r'(\d+)(K|M|G|Ki|Mi|Gi)?', bs_str)
	if m :
		val = m.group(1)
		unit = m.group(2)
		if unit == 'K' :
			bs = int(m.group(1)) * 1000
		elif unit == 'Ki' :
			bs = int(m.group(1)) * 1024
		elif unit == 'M' :
			bs = int(m.group(1)) * 1000 * 1000
		elif unit == 'Mi' :
			bs = int(m.group(1)) * 1024 * 1024
		elif unit == 'G' :
			bs = int(m.group(1)) * 1000 * 1000 * 1000
		elif unit == 'Gi' :
			bs = int(m.group(1)) * 1024 * 1024 * 1024
		elif not unit :
			bs = int(m.group(1))
		else :
			printf('invalid unit for "{0}"'.format(bs_str))
			sys.exit(1)
	else :
		print('invalid block size, {0}'.format(bs_str))
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
	
	table = 'fio_table'
	#fp = open(output, mode='w', encoding='utf-8')
	conn = sqlite3.connect(output)
	
	create_table(conn, table)

	for filepath in args:
		print('read {0}'.format(filepath))

		fp_in = open(filepath, mode='r', encoding='utf-8')
		data = json.load(fp_in)
		fp_in.close()

		
		if 'format' in data and data['format'] == 'normal' :
			fmt = 'normal'
		else :
			fmt = 'json'

		for job in data['jobs'] :
			rw = job['job options']['rw']
			bs = str(job['job options']['bs'])
			
			print('bs is {0}'.format(bs))

			bs = normalize_blocksize(bs)

			name = job['jobname']
			if re.search(r'read', rw) :
				bw = int(job['read']['bw'])
			else :
				bw = int(job['write']['bw'])

			m = re.search(r'(\w+)-(\w+)-([\w\d]+)', name)
			if m :
				env = m.group(1)
			else :
				print('invalid name, {0}'.format(name))
				sys.exit(1)
		
			record = {
				'name' : name,
				'env'  : env,
				'fmt' : fmt,
				'rw'   : rw,
				'bs'   : bs,
				'bw'   : bw
			}

			insert_record(conn, table, record)	

	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	main()
