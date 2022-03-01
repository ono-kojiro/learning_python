#!/usr/bin/python3

import sys

import getopt
import json

import re

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

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
    sql += 'rw INTEGER, '
    sql += 'bs INTEGER, '
    sql += 'bw INTEGER '
    sql += ');'

    c.execute(sql)

def insert_record(conn, table, record):
    c = conn.cursor()
    sql = 'INSERT INTO {0} VALUES ( NULL, ?, ?, ?, ? );'.format(table)
    list = [ 
        record['name'],
        record['rw'],
        record['bs'],
        record['bw']
    ]

    c.execute(sql, list)

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
            "hvo:",
            [
              "help",
              "version",
              "output="
            ]
        )
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
	fp.write('# name, rw, bs, bw\n')
	for database in args:
		table = 'fio_table'
		conn = sqlite3.connect(database)
		conn.row_factory = sqlite3.Row

		sql = 'SELECT name, rw, bs, bw FROM {0}'.format(table)
		sql += ' ORDER BY rw ASC, bs ASC;'

		c = conn.cursor()
		rows = c.execute(sql)

		last_rw   = ''

		for row in rows :
			name = row['name']
			rw   = row['rw']
			bs   = int(row['bs'])
			bw   = int(row['bw'])

			if last_rw != '' and last_rw != rw :
				fp.write('\n')
			fp.write('{0:20}\t{1:10}\t{2:10}\t{3:10}\n'.format(
				name, rw, bs, bw))

			last_rw = rw

		conn.close()

	fp.close()

if __name__ == "__main__":
	main()
