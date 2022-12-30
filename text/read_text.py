#!/usr/bin/env python3

import sys
import re

import getopt

import jaconv

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

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        while 1 :
            line = fp_in.readline()
            if not line :
                break

            line = re.sub(r'\r?\n?$', '', line)

            line = jaconv.z2h(line, kana=False, digit=True, ascii=True)
            line = jaconv.h2z(line, kana=True,  digit=False, ascii=False)

            fp.write("LINE : {0}\n".format(line))

        fp_in.close()
    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

