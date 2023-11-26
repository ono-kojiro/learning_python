#!/usr/bin/python

import sys
import re

import getopt

import json
import yaml
from yaml.loader import SafeLoader

from pprint import pprint


def usage():
    print("Usage : {0}".format(sys.argv[0]))

def read_json(filepath):
    fp = open(filepath, mode='r', encoding='utf-8')
    data = json.load(fp)
    fp.close()
    return data

def read_yaml(filepath):
   fp = open(filepath, mode="r", encoding="utf-8")
   data = yaml.load(fp, Loader=SafeLoader)
   fp.close()

   return data

def get_items(top, tokens):
    pos = top

    for token in tokens :
        if token in pos :
            pos = pos[token]
        else :
            pos = None
            break

    return pos

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
    
    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(1)
   
    for filepath in args:
        data = read_json(filepath)

    ifnumber = 0
    # IF-MIB:ifNumber.0
    if 'IF-MIB' in data :
        if 'ifNumber.0' in data['IF-MIB'] :
            ifnumber = data['IF-MIB']['ifNumber.0']
   
    print('ifnumber: {0}'.format(ifnumber))

    items = get_items(data, [ 'IF-MIB', 'ifName' ])
    if items:
        for ifid in items :
            typ = items[ifid]['typ']
            val = items[ifid]['val']

            print('{0}, {1}'.format(ifid, val))
    else :
        print('ERROR: IF-MIB::ifName not found')

    items = get_items(data, [ 'RFC1213-MIB', 'ipNetToMediaIfIndex' ])
    if items :
        for ifid in items :
            for addr in items[ifid] :
                print('{0}, {1}'.format(ifid, addr))


    #yaml.dump(data,
    #    fp,
    #    allow_unicode=True,
    #    default_flow_style=False,
    #    sort_keys=True,
    #)

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

