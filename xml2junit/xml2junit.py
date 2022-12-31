#!/usr/bin/env python3

import sys
import getopt

from lxml import etree

def main() :
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:x:",
            [
                "help",
                "version",
                "output=",
                "xsl=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    output = None
    xslfile = None

    for option, arg in options:
        if option in ("-v", "-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-x", "--xsl"):
            xslfile = arg
        elif option in ("-o", "--output"):
            output = arg
        else:
            assert False, "unknown option"

    if xslfile is None :
        print('no xsl option')
        sys.exit(1)

    if ret != 0:
        sys.exit(1)

    if output is not None:
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    xsl = etree.parse(xslfile)

    for filepath in args :
        dom = etree.parse(filepath)

        transform = etree.XSLT(xsl)

        newdom = transform(dom)

        decoded = etree.tostring(newdom, pretty_print=True).decode()
        fp.write(decoded)

    if output is not None :
        fp.close()

if __name__ == "__main__" :
    main()

