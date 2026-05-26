#!/usr/bin/env python3

import sys
import re

import getopt

import yaml

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def generate_model(fp, data):
    for name, model_def in data["models"].items():
        fp.write("class {0}(models.Model):\n".format(name))
        
        for fname, field_def in model_def["fields"].items():
            ftype = field_def["type"]
            args = ""
            for k, v in field_def.items():
                if k == "type":
                    continue
                if k is None:
                    k = 'null'
                args += ", {0}={1}".format(k, v)

            args = re.sub(r'^, ', '', args)
            fp.write('    {0} = models.{1}({2})\n'.format(fname, ftype, args))

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
        for model in data['models']:
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

