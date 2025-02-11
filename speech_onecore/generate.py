#!/usr/bin/env python

import sys
import getopt

import re

import win32com.client

def usage():
	print("Usage : {0}".format(sys.argv[0]))

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
	
	if output is None :
		print("no output option")
		ret += 1
	
	if ret != 0:
		sys.exit(1)

	name = "Microsoft Sayaka"
	
	sapi = win32com.client.Dispatch("SAPI.SpVoice")
	cat  = win32com.client.Dispatch("SAPI.SpObjectTokenCategory")
	cat.SetID(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices", False)
	v = [t for t in cat.EnumerateTokens() if t.GetAttribute("Name") == name]
	if not v:
		print('ERROR: can not find {0}'.format(name))
		sys.exit(1)
		
	fs = win32com.client.Dispatch("SAPI.SpFileStream")
	fs.Open(output, 3)
	sapi.AudioOutputStream = fs
	oldv = sapi.Voice
	sapi.Voice = v[0]

	for arg in args :
		fp = open(arg, 'r', encoding='utf-8')
		while 1:
			line = fp.readline()
			if not line:
				break
			line = re.sub(r'\r?\n?$', '', line)
			if line != "" :
				print('INFO: {0}'.format(line))
				sapi.Speak(line)
		fp.close()
	sapi.Voice = oldv
	fs.Close()

if __name__ == "__main__":
	main()
