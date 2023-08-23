#!/usr/bin/env python3

import sys
import re

import getopt

from ldif import LDIFParser, LDIFWriter

def usage():
    print("Usage : {0} -o outfile infile ..".format(sys.argv[0]))

class Parser(LDIFParser):
    def __init__(self, fp_in, fp_out):
        LDIFParser.__init__(self, fp_in)
        self.writer = LDIFWriter(fp_out)
        self.skip = 1
    
    def handle(self, dn, entry):
        if not self.skip :
            self.writer.unparse(dn, entry)

        if re.search(r'ou=Idmap,', dn) :
            self.skip = 0

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
        parser = Parser(fp_in, fp)
        parser.parse()
        fp_in.close()

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

