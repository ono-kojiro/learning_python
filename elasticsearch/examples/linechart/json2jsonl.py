#!/usr/bin/env python3

import sys

import getopt
import json

from pprint import pprint

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvo:n:",
            [
                "help",
                "version",
                "output=",
                "name=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
	
    output = None
    name   = None

    for o, a in opts:
        if o == "-v":
            usage()
            sys.exit(0)
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-n", "--name"):
            name = a
        else:
            assert False, "unknown option"
	
    if output is not None :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout
    
    #if name is None:
    #    pprint(args)
    #    print('ERROR: no name option', file=sys.stderr)
    #    ret += 1
	
    if ret != 0:
        sys.exit(1)

    name = "linechart"

    for filepath in args:
        fp_in = open(filepath, mode='r', encoding='utf-8')
        items = json.load(fp_in)
        fp_in.close()

        i = 1
        for item in items:
            #for key in item.keys() :
            #    val = item[key]
            #    print('key: {0}, val: {1}'.format(key, val))
            _id = '{0}-{1:03}'.format(name, i)
            print('{{"index": {{"_id": "{0}"}}}}'.format(_id))

            print(
                json.dumps(
                    item,
	                #indent=4,
                    ensure_ascii=False
                )
            )

            i += 1
            
    if output is not None :
        fp.close()
	
if __name__ == "__main__":
	main()
