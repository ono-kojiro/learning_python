#!/usr/bin/env python3

import sys
import re

import getopt

import yaml

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()

    return data

def get_related_models(model_defs):
    related = {}
    for name, model_def in model_defs.items():
        rels = []
        for fname, field_def in model_def["fields"].items():
            if field_def["type"] in ["ForeignKey", "OneToOneField"]:
                rels.append(field_def["to"])
        related[name] = rels
    return related

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:d:",
            [
                "help",
                "version",
                "output=",
                "depend=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    depend_yml = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-d", "--depend"):
            depend_yml = optarg
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if depend_yml is None:
        print('ERROR: no depend option', file=sys.stderr)
        sys.exit(1)

    if ret != 0:
        sys.exit(ret)

    deps = read_yaml(depend_yml)

    model_defs = {}

    fp.write('from rest_framework import serializers\n')

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)
        
        model = data['name']

        fp.write('from myapp.models import {0}\n'.format(model))
        fp.write('\n')

        for dep in deps['dependencies'][model]:
            fp.write('from myapp.serializers import {0}Serializer\n'.format(dep))

        fp.write('\n')
        fp.write('class {0}Serializer(serializers.ModelSerializer):\n'.format(
            model))

        for fname, field_def in data['fields'].items():
            if field_def['type'] in [ 'ForeignKey', 'OneToOneField']:
                to_model = field_def['to']
                fp.write('    {0} = {1}Serializer(read_only=True)\n'.format(
                    fname, to_model))

        fp.write('\n')
        fp.write('    class Meta:\n')
        fp.write('        model = {0}\n'.format(model))
        fp.write('        fields = "__all__"\n')
        fp.write('\n')
        
        fp_in.close()

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

