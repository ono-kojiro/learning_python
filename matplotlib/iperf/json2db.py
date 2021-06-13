#!/usr/bin/python3

import sys

import getopt
import json

import sqlite3

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def read_json(filepath) :
	fp = open(filepath, mode='r', encoding='utf-8')
	data = json.load(fp)
	fp.close()
	return data

def format_bytes(size):
	# 2**10 = 1024
	power = 2**10
	n = 0
	power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
	while size > power:
		size /= power
		n += 1
	return size, power_labels[n]+'bytes'

def read_bitrate(data):
	connected_0 = data['start']['connected'][0]
	test_start = data['start']['test_start']

	local_host  = connected_0['local_host']
	local_port  = connected_0['local_port']
	remote_host = connected_0['remote_host']
	remote_port = connected_0['remote_port']
	
	blksize     = test_start['blksize']

	'''
	print("{0}:{1} => {2}:{3}, {4}".format(
		local_host, local_port,
		remote_host, remote_port,
		blksize))
	'''

	sum_sent = data['end']['sum_sent']
	sum_received = data['end']['sum_received']

	bps_client = sum_sent['bits_per_second']
	sender = sum_sent['sender']

	server_data = data['server_output_json']
	sum_sent = server_data['end']['sum_sent']
	sum_received = server_data['end']['sum_received']

	bps_server = sum_received['bits_per_second']

	return str(blksize), bps_server

def create_table(conn, table):
    c = conn.cursor()

    sql = 'DROP TABLE IF EXISTS {0};'.format(table)
    c.execute(sql)

    sql = 'CREATE TABLE {0} ('.format(table)
    sql += 'id INTEGER PRIMARY KEY, '
    sql += 'name TEXT, '
    sql += 'env TEXT, '
    sql += 'bps INTEGER '
    sql += ');'

    c.execute(sql)

def insert_record(conn, table, record):
    c = conn.cursor()
    sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ? );'.format(table)
    list = [
        record['name'],
        record['env'],
        record['bps']
    ]

    c.execute(sql, list)

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
	
	#if output == None :
	#	fp = sys.stdout
	#else :
	#	fp = open(output, mode='w', encoding='utf-8')
	conn = sqlite3.connect(output)
	table = 'fio_table'
	create_table(conn, table)

	blksizes = {
		'4096' : '4K',
		'8192' : '8K',
		'16384' : '16K',
		'32768' : '32K',
		'65536' : '64K',
		'131072' : '128K',
		'262144' : '256K',
		'524288' : '512K',
		'1048576' : '1024K',
	}

	records = {}

	for filepath in args:
		data = read_json(filepath)
		blksize, bps = read_bitrate(data)
		if blksize in blksizes :
			blksize = blksizes[blksize]
		else :
			print('invalid blksize, {0}'.format(blksize))
			sys.exit(1)

		bytes_per_second = bps / 8.0
		byte_rate = format_bytes(bytes_per_second)

		record = {
			'name' : blksize,
			'env'  : 'host',
			'bps'  : int(bps),
		}
		insert_record(conn, table, record)

	#if output == None :
	#	pass
	#else :
	#	fp.close()
	conn.commit()
	conn.close()

	print(records)

if __name__ == "__main__":
	main()
