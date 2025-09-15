#!/usr/bin/env python3

import sys

import getopt
import json

from pprint import pprint

def usage():
    print("Usage : {0}".format(sys.argv[0]))

def print_array(name, items):
    i = 1
    _id = '{0}-{1:03}'.format(name, i)
    print('{{"index": {{"_id": "{0}"}}}}'.format(_id))

    #data = {
    #    'type': name,
    #    name: items,
    #}
    print(
        json.dumps(
            items,
            #indent=4,
            ensure_ascii=False
        )
    )
    print('')

def print_jsonl(name, items):
    i = 1
    for item in items:
        #for key in item.keys() :
        #    val = item[key]
        #    print('key: {0}, val: {1}'.format(key, val))
        _id = '{0}-{1:03}'.format(name, i)
        print('{{"index": {{"_id": "{0}"}}}}'.format(_id))

        if name is not None:
            item['type'] = name

        #data = {
        #    name : item
        #}

        print(
            json.dumps(
                item,
	            #indent=4,
                ensure_ascii=False
            )
        )
        print('')

        i += 1

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
    
	
    for filepath in args:
        fp_in = open(filepath, mode='r', encoding='utf-8')
        items = json.load(fp_in)
        fp_in.close()

        #print_jsonl(name, items)
        print_array(name, items)
            
    if output is not None :
        fp.close()
	
if __name__ == "__main__":
	main()
