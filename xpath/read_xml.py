#!/usr/bin/env python3

import os
import sys
import re

import getopt
import json

from datetime import datetime
import dateutil.parser

import xml.etree.ElementTree as ET

from pprint import pprint

def usage():
    print("Usage : {0} [-o output.json] [input.xml]".format(sys.argv[0]))

def parse_xml(fp, filepath) :
    tree = ET.parse(filepath)
    root = tree.getroot()

    pprint(root)
    m = re.search(r'\{(.+)\}', root.tag)
    if m :
        ns = m.group(1)
    else :
        print('ERROR : can not get namespace')
        sys.exit(1)

    # namepaces
    nss = { "ns" : ns }

    items = root.findall(".//ns:CHILD/..", nss)
    for item in items :
        child    = item.find("./ns:CHILD", nss).text
        name     = item.find("./ns:NAME", nss)
        value    = item.find("./ns:VALUE", nss)
        ref      = item.find("./ns:REF", nss)

        if name is not None:
            name = name.text
        else :
            name = ''

        text = ''
        if value is not None:
            text = value.text
        if valref is not None:
            text = valref.text

        if text is not None:
            print('{0}, {1}, {2}'.format(name, ref, text))

def main():
    ret = 0

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hvi:o:d",
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
        print('read {0}'.format(filepath))
        parse_xml(fp, filepath)
    
    if output is not None :
        fp.close()
    
if __name__ == "__main__":
    main()

