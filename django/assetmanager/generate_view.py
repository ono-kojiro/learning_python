#!/usr/bin/env python3

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

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)


    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)
        fp.write('from rest_framework import viewsets\n')
        
        model = data['name']

        fp.write('from myapp.models import {0}\n'.format(model))
        serializer = model + 'Serializer'
        fp.write('from myapp.serializers import {0}\n'.format(serializer))

        fp.write('\n')
        fp.write('class {0}ViewSet(viewsets.ModelViewSet):\n'.format(model))
        fp.write('    queryset = {0}.objects.all()\n'.format(model))
        fp.write('    serializer_class = {0}\n'.format(serializer))

        fp_in.close()

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

