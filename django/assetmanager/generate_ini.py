#!/usr/bin/env python3

import os
import sys
import re

import getopt

import yaml

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        else:
            assert False, "unknown option"

    if ret != 0:
        sys.exit(ret)

    items = []

    for filepath in args:
        filename = os.path.basename(filepath)
        if filename == '__init__.py' :
            continue

        module = re.sub(r'\.py$', '', filename)

        fp_in = open(filepath, mode="r", encoding="utf-8")
        while 1:
            line = fp_in.readline()
            if not line:
                break

            line = re.sub(r'\r?\n?$', '', line)
            m = re.search(r'^class\s+(\w+)', line)
            if m :
                name = m.group(1)
                item = {
                    'module': module,
                    'class': name,
                }
                items.append(item)

        fp_in.close()
    
    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    for item in sorted(items, key=lambda d: d['class']):
        module = item['module']
        name   = item['class']
        fp.write('from .{0} import {1}\n'.format(module, name))

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

