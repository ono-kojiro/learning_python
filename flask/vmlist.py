#!/usr/bin/env python3

import sys
import re

import json

import getopt

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

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    items = []

    for filepath in args:
        if filepath != '-' :
            fp_in = open(filepath, mode="r", encoding="utf-8")
        else :
            fp_in = sys.stdin

        b_first = 1
        colnames = []
        while 1 :
            line = fp_in.readline()
            if not line :
                break

            line = re.sub(r'\r?\n?$', '', line)

            if b_first:
                colnames = re.split(r'\s{2,}', line)
                b_first = 0
            else :
                tokens = re.split(r'\s{2,}', line)
                item = {}
                for i in range(len(colnames)):
                    colname = colnames[i]
                    token   = tokens[i]
                    item[colname] = token
                items.append(item)

        if filepath != '-' :
            fp_in.close()
    fp.write(
        json.dumps(
            items,
            indent=4,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    fp.write('\n')

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

