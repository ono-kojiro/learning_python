#!/usr/bin/env python3

import sys
import re

import getopt

import yaml

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def extract_depend(data):
    deps = []

    fields = data.get('fields', {})
    for field_name, field_def in fields.items():
        ftype = field_def.get('type')
        if ftype in ('ForeignKey', 'OneToOneField'):
            deps.append(field_def['to'])

    return deps

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

    dep_map = {}

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)
        deps = extract_depend(data)

        model = data['name']

        dep_map[model] = deps
        fp_in.close()

    fp.write('---\n')
    fp.write(
        yaml.dump(
            {
                'dependencies': dep_map,
            },
            sort_keys=True,
            allow_unicode=True,
        )
    )

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

