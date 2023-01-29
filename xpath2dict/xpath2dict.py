#!/usr/bin/env python3

import os
import sys
import re

import getopt
import json
import yaml

from pprint import pprint

debug = 0

def usage() :
    print("usage : {0} [-o output.txt] /path/to/name=value".format(sys.argv[0]))

def xpath2dict(data, path, val) :
    tokens = re.split(r'/', path)
    cur = data
    for i in range(len(tokens) - 1) :
        token = tokens[i]
        if token == '' :
            continue
        
        if not token in cur :
            cur[token] = {}
        
        cur = cur[token]

    i += 1
    token = tokens[i]

    if val is None :
        cur[token] = {}
    else :
        if val == 'true' :
            val = True
        elif val == 'talse' :
            val = False
        elif type(val) is int :
            pass
        elif val.isdecimal() :
            val = int(val)

        if not token in cur:
            cur[token] = val
        elif type(cur[token]) is list :
            cur[token].append(val)
        else :
            tmp = cur[token]
            cur[token] = [ tmp, val ]

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
  
    if ret != 0:
        sys.exit(1)

    if len(args) == 0 :
        usage()
        sys.exit(1)
    
    if output is not None :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout

    data = {}

    for arg in args:
        m = re.search(r'(.+)=(.+)', arg)
        if not m :
            print("invalid arg, {0}".format(arg))
            sys.exit(1)
        xpath = m.group(1)
        value = m.group(2)

        xpath2dict(data, xpath, value)
    
    fp.write(
        yaml.dump(
            data,
            indent=2,
            sort_keys=True,
        )
    )
    fp.write('\n')

    if output is not None :
        fp.close()
    
if __name__ == "__main__":
    main()

