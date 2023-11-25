#!/usr/bin/python

import sys
import re

import getopt

def usage():
    print("Usage : {0}".format(sys.argv[0]))

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
   
    count = 0
    for filepath in args:
        print('open {0}'.format(filepath))
        fp_in = open(filepath, mode="r", encoding="utf-8")
        while True:
            line = fp_in.readline()
            if not line:
                break
            count += 1

            line = re.sub(r'\r?\n?$', '', line)

            oid = None
            val = None
            typ = None
            m = re.search(r'^([\w\-]+::[\w\-]+)(.*) = (.+: )?(.+)?', line)
            if m :
                oid = m.group(1)
                name = m.group(2)
                typ = m.group(3)
                val = m.group(4)
            else :
                print('line: {0}'.format(count))
                print('invalid line, {0}'.format(line))
                sys.exit(1)

            if val is None :
                val = ""

            m = re.search(r'^"(.+)"$', val)
            if m :
                val = m.group(1)
            print("{0}, {1}, {2}, {3}".format(oid, name, typ, val))

        fp_in.close()
        
    if output is not None:
        fp_out.close()

if __name__ == "__main__":
    main()

