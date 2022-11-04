#!/usr/bin/python3

import sys
import os

import getopt
import codecs

import re

def usage():
	prog=os.path.basename(sys.argv[0])
	print("Usage : {0} -e PATTERN [FILE...]".format(prog))

class MyIterator():
    def __init__(self) :
        self.count = 0
    def __iter__(self) :
        return self
    def __next__(self) :
        filepath = None
        while True :
            line = sys.stdin.readline()
            if not line :
                raise StopIteration()

            line = re.sub(r'\r?\n?$', '', line)
            if os.path.isfile(line) :
                filepath = line
                break

        self.count += 1
        return filepath


def main():
	ret = 0
	
	try:
		opts, args = getopt.getopt(
   			sys.argv[1:],
			"hvo:e:",
			[
				"help",
				"version",
				"output=",
				"expr=",
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = None
	expr   = None
	
	for o, a in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-e", "--expr"):
			expr = a
		elif o in ("-o", "--output"):
			output = a
	
	ret = 0

	if expr == None :
		print('no expr option')
		ret += 1

	if ret != 0:
		sys.exit(1)

	if output == None :
		fp = sys.stdout
	else :
		fp = open(output, mode='w', encoding='utf8')

	#if len(args) == 0:
	#	usage()
	#	sys.exit(1)

	#if expr == None :
	#	expr = args[0]
	#	args = args[1:]
	
	p = re.compile(expr)

	if len(args) == 0 :
		#files = [ '-' ]
		files = MyIterator()
	else :
		files = args

	count = 0
	for filepath in files:
		count += 1

		#print('{0}'.format(filepath))
		fp_in = open(filepath, mode='rb')

		line_num = 0
		b_first = 1
		while 1:
			line = fp_in.readline()
			if not line :
				break

			line_num += 1

			try :
				line = line.decode('utf-8')
			except UnicodeDecodeError:
				continue

			line = line.rstrip()
			line = re.sub(r'#.*', '', line)   

			if p.search(line) :
				if b_first :
					b_first = 0
					fp.write('{0}\n'.format(filepath))

				fp.write('   LINE {0} : '.format(line_num) + line + '\n')
		
		if filepath != '-' :
			fp_in.close()

	print('INFO : read {0} files'.format(count))
	fp.close()

if __name__ == "__main__":
	main()

