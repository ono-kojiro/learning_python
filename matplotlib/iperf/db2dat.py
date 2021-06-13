#!/usr/bin/python3

import sys

import getopt
import json

import re

import sqlite3

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
	fp.write('# name, env, bps\n')
	for database in args:
		table = 'iperf_table'
		conn = sqlite3.connect(database)
		conn.row_factory = sqlite3.Row

		sql = 'SELECT name, env, bps FROM {0}'.format(table)
		sql += ' ORDER BY env ASC, bps ASC;'

		c = conn.cursor()
		rows = c.execute(sql)

		last_env   = ''

		for row in rows :
			name = row['name']
			env  = row['env']
			bps  = int(row['bps'])

			if last_env != '' and last_env != env :
				fp.write('\n')
			fp.write('{0}\t{1}\t{2}\n'.format(
				name, env, bps))

			last_env = env

		conn.close()

	fp.write('\n')
	fp.close()

if __name__ == "__main__":
	main()
