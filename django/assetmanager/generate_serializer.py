#!/usr/bin/env python3

import sys
import re

import getopt

import yaml

from pprint import pprint

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def read_yaml_list(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        docs = list(yaml.safe_load_all(fp))
    return docs

def read_yaml_dict(filepath):
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
                #"all-models=",
                #"model=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    depend_yml = None
    all_models_yaml = None
    #model = None

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
        #elif option in ("-a", "--all-models"):
        #    all_models_yaml = optarg
        #elif option in ("-m", "--model"):
        #    model = optarg
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if depend_yml is None:
        print('ERROR: no depend option', file=sys.stderr)
        ret += 1
    #if all_models_yaml is None:
    #    print('ERROR: no all-models option', file=sys.stderr)
    #    ret += 1
    #if model is None:
    #    print('ERROR: no model option', file=sys.stderr)
    #    ret += 1

    if ret != 0:
        sys.exit(ret)

    #docs = read_yaml_list(all_models_yaml)
    #model_map = { doc["name"]: doc for doc in docs }

    deps = read_yaml_dict(depend_yml)
    pprint(deps)

    model_defs = {}

    fp.write('from rest_framework import serializers\n')

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)
        
        model = data['name']

        for dep in deps['dependencies'][model]:
            fp.write('from myapp.models import {0}\n'.format(dep))
        fp.write('from myapp.models import {0}\n'.format(model))

        fp.write('\n')

        for dep in deps['dependencies'][model]:
            fp.write('from myapp.serializers import {0}Serializer\n'.format(dep))

        fp.write('\n')
        fp.write('class {0}Serializer(serializers.ModelSerializer):\n'.format(
            model))
        
        for fname, field_def in data['fields'].items():
            pprint(field_def)
            if field_def['type'] in [ 'ForeignKey', 'OneToOneField']:
                to_model = field_def['to']
                fp.write('    # for read\n')
                fp.write('    {0} = {1}Serializer(read_only=True)\n'.format(
                    fname, to_model))
                fp.write('\n')
                fp.write('    # for write\n')
                fp.write('    {0}_id = serializers.PrimaryKeyRelatedField(\n'.format(fname))
                fp.write('        queryset={0}.objects.all(),\n'.format(to_model))
                fp.write('        write_only=True,\n')

                null_allowed = field_def.get("null", field_def.get(None, False))
                blank_allowed = field_def.get("blank", False)

                allow_null = "True" if null_allowed else "False"
                required = "False" if (null_allowed or blank_allowed) else "True"

                fp.write('        allow_null={0},\n'.format(allow_null))
                fp.write('        required={0},\n'.format(required))
                fp.write('    )\n')
                fp.write('\n')

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

