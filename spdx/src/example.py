#!/usr/bin/env python3

import sys
import re

import getopt

from spdx.parsers.tagvalue import Parser
from spdx.parsers.tagvaluebuilders import Builder
from spdx.parsers.loggers import StandardLogger

def read_lines(filepath) :	
	fp = open(filepath, mode='r', encoding='utf-8')

	lines = ''
	while True :
		line = fp.readline()
		if not line :
			break

		line = re.sub(r'\r?\n?$', '', line)
		lines += line + '\n'

	fp.close()
	return lines

def main():
	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvo:s:",
			[
				"help",
				"version",
				"schema=",
				"output="
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)

	output = None

	for o, a in opts:
		if o in ('-o', '--output') :
			output = a
		else :
			assert False, "unhandled option"

	if output is not None:
		fp = open(output, mode='w', encoding='utf-8')
	else :
		fp = sys.stdout

	p = Parser(Builder(), StandardLogger())
	p.build()

	# data is a string containing the SPDX file.

	for arg in args :
		lines = read_lines(arg)

		document, error = p.parse(lines)

if __name__ == '__main__' :
	main()

