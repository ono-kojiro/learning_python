#!/usr/bin/python3

import sys

import getopt
import json
import re

import email

from email.parser import Parser

from bs4 import BeautifulSoup
from html.parser import HTMLParser

import quopri
from lxml import etree
from io import StringIO, BytesIO

from pprint import pprint

import io
# 3.6 =< 3.x
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def usage():
	print("Usage : {0}".format(sys.argv[0]))

def read_json(filename) :
	fp = open(filename, mode='r', encoding='utf-8')
	data = json.load(fp)
	fp.close()
	return data

def print_events(events) :
	for action, obj in events :
		if action in ('start', 'end') :
			pass
		elif action == 'start-ns' :
			pass
	
def extract_head(payload) :
	lines = ''
	b_in_head = 0
	
	for line in payload.splitlines() :
		if re.search('</head>', line) :
			b_in_head = 0

		if b_in_head :
			lines = lines + line + '\n'

		if re.search('<head>', line) :
			b_in_head = 1
	
	return lines

def extract_body(payload) :
	lines = ''
	b_in_body = 0
	
	for line in payload.splitlines() :
		if re.search('</body>', line) :
			b_in_body = 0

		if b_in_body :
			lines = lines + line + '\n'

		if re.search('<body>', line) :
			b_in_body = 1
	
	return lines

def get_content(part) :
	charset = part.get_content_charset()
	payload = part.get_payload(decode=True)
	try :
		if payload :
			if charset :
				return payload.decode(charset)
			else :
				return payload.decode()
		else:
			return ""
	except:
		return payload

def main():
	ret = 0

	try:
		opts, args = getopt.getopt(
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
	
	if len(args) == 0:
		print('no input file')
		sys.exit(1)
		
	bodies = []
	parts = []

	for filepath in args :
		fp_in = open(filepath, mode='r', encoding='utf-8')
		parser = Parser()
		msg = parser.parse(fp_in, headersonly=False)
		for part in msg.walk() :
			if part.is_multipart() :
				pass
			else :
				payload = part.get_payload(decode=False)
				body = extract_body(payload)
				if body and len(body) :
					bodies.append(body)
				else :
					parts.append(part)
		fp_in.close()

	fp = open(output, mode='w', encoding='utf-8')

	while True :
		filepath = args[0]

		fp_in = open(filepath, mode='r', encoding='utf-8')
		
		parser = Parser()
		msg = parser.parse(fp_in, headersonly=False)
		
		b_first = 1
		for part in msg.walk() :
			for key in part.keys() :
				val = part[key]
				fp.write("{0}: {1}\n".format(key, val))
			fp.write('\n')
			
			if part.is_multipart() :
				pass
			else :
				head = extract_head(part.get_payload(decode=False))
				payload = part.get_payload(decode=True)
				soup = BeautifulSoup(payload, "html.parser")
				
				if b_first :
					fp.write("<html xmlns:o=3D'urn:schemas-microsoft-com:office:office'\n")
					fp.write("      xmlns:w=3D'urn:schemas-microsoft-com:office:word'\n")
					fp.write("      xmlns:v=3D'urn:schemas-microsoft-com:vml'\n")
					fp.write("      xmlns=3D'urn:w3-org-ns:HTML'>\n")
					
					fp.write('<head>\n')
					fp.write(head + '\n')
					fp.write('</head>\n')
					
				if b_first :
					b_first = 0
					fp.write('<body>\n')
					for body in bodies :
						fp.write("{0}\n".format(body))
						fp.write("<br clear=all style='mso-special-character:line-break;page-break-before:always'>\n")
					fp.write('</body>\n')

				fp.write('</html>\n')

			boundary = part.get_boundary()
			if boundary :
				fp.write("--{0}\n".format(boundary))
		
		boundary = msg.get_boundary()

		for part in parts :
			fp.write("--{0}\n".format(boundary))
			fp.write("{0}\n".format(part))
			
		fp.write("--{0}--\n".format(boundary))
			
		fp_in.close()
		break
	
	fp.close()
	
if __name__ == "__main__":
	main()
