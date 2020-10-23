#!/usr/bin/python3

import sys

import getopt
import json

import re

from lxml import etree
from io import StringIO, BytesIO

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def parse_events(parser) :
    for action, elem in parser.read_events() :
        if action in ('start', 'end') :
            sys.stdout.write("action '{0}', ".format(action))
            sys.stdout.write("tag '{0}', ".format(elem.tag))
            sys.stdout.write("text '{0}'".format(elem.text))
            print("")
        elif action == 'start-ns':
            print('{0} : {1}'.format(action, elem))
        else:
            print(action)

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

    event_types = (
        "start", "end", "start-ns", "end-ns",
        "comment", "pi"
    )

    for input in args:
        print("arg : {0}".format(input))

        
        fp_in = open(input, mode='r', encoding='utf-8')
       
        parser = etree.XMLPullParser(
            events=event_types
        )

        while 1:
            line = fp_in.readline()
            if not line :
                break

            line = re.sub(r'\r?\n?$', '', line)
            print('feed : {0}'.format(line))

            parser.feed(line)
            parse_events(parser)

        parse_events(parser)

        #print(
        #    json.dumps(
        #        data,
	#        indent=4,
        #        ensure_ascii=False
        #    )
        #)
        
        fp_in.close()
	
    fp.close()
	
if __name__ == "__main__":
	main()
