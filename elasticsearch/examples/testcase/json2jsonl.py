#!/usr/bin/env python3

import os
import sys
import re

import getopt

import json

from datetime import datetime
import dateutil.parser

from pprint import pprint

def usage():
    print("Usage : {0} [-o output.jsonl] [input.xml]".format(sys.argv[0]))

def read_json(filepath) :
    fp = open(filepath, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

def json2jsonl(fp, data) :
    count = 0

    for testcase in data['testcases'] :
        count += 1

        index_data = {
            "index" : {
                "_id" : testcase['id']
            }
        }

        fp.write(
            json.dumps(
                index_data,
                ensure_ascii=False,
            )
        )
        fp.write('\n')
        
        fp.write(
            json.dumps(
                testcase,
                ensure_ascii=False,
            )
        )
        fp.write('\n')

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
    
    if ret != 0:
        sys.exit(1)

    if len(args) == 0 :
        usage()
        sys.exit(1)
    
    if output is not None :
        fp = open(output, mode='w', encoding='utf-8')
    else :
        fp = sys.stdout

    for filepath in args:
        data = read_json(filepath)
        json2jsonl(fp, data)
    
    if output is not None :
        fp.close()
    
if __name__ == "__main__":
    main()

