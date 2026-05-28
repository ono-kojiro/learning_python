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

        
    fp.write('from rest_framework import routers\n')

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)

        model = data['name']

        fp.write('from myapp.views.{0}_view import {1}ViewSet\n'.format(
            model.lower(), model))

        fp.write('\n')
        fp.write('router = routers.DefaultRouter()\n')
        fp.write('\n')

        fp.write('router.register(r"{0}s", {1}ViewSet)\n'.format(
            model.lower(), model))
        fp.write('\n')
        fp.write('urlpatterns = router.urls\n')
        
        fp_in.close()

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

