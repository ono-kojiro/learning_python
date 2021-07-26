#!/usr/bin/env python3

import sys
import getopt

import json
import csv

def usage() :
	print('Usage : {0} -o <output> <input>...'.format(sys.argv[0]))

def main() :
	ret = 0

	try :
		options, args = getopt.getopt(
			sys.argv[1:],
			"hvo:",
			[
				"help",
				"version",
				"output=",
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(1)

	output = None

	for option, optarg in options:
		if option == "-v" :
			usage()
			sys.exit(1)
		elif option in ("-h", "--help"):
			usage()
			sys.exit(1)
		elif option in ("-o", "--output"):
			output = optarg
		else:
			assert False, "unknown option"

	#if output == None :
	#	print('no output option')
	#	ret += 1

	if ret != 0 :
		sys.exit(ret)

	if output == None :
		fp = sys.stdout
	else :
		fp = open(output, mode='w', encoding='utf-8')

	for csvfile in args:
		records = []
		fp_in = open(csvfile, newline='')
		reader = csv.reader(fp_in, delimiter=',', quotechar='|')

		# reader to records
		for row in reader:
			if len(row) == 0 :
				continue
			records.append(row)
		fp_in.close()

		tmp = {}
		ids = []
		for record in records :
			row_id = record[0]
			if not row_id in tmp :
				tmp[row_id] = 1
				ids.append(row_id)

		targets = ids
		if len(targets) > 2 :
			targets = targets[:-2]

		for record in records:
			if len(record) == 0 :
				continue
			row_id = record[0]
			if row_id in targets:
				fp.write(', '.join(record) + '\n')
				

	if output != None :
		fp.close()



if __name__ == "__main__" :
	main()

