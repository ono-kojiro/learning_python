#!/usr/bin/env python3

import sys
import re

import getopt

import yaml

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def extract_depend(models):

    res = {}
    for model_name, model_def in models.items():
        deps = []

        fields = model_def.get('fields', {})
        for field_name, field_def in fields.items():
            ftype = field_def.get('type')
            if ftype in ('ForeignKey', 'OneToOneField'):
                deps.append(field_def['to'])
        res[model_name] = deps

    return res

def resolve_depend(target, deps, resolved=None, visited=None):
    if resolved is None:
        resolved = []
    if visited is None:
        visited = set()

    if target in visited:
        return resolved

    visited.add(target)

    for dep in deps.get(target, []):
        resolve_depend(dep, deps, resolved, visited)

    if target not in resolved:
        resolved.append(target)

    return resolved

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
        #print('INFO: read {0}'.format(filepath))
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)
        #print(data)
        deps = extract_depend(data['models'])

        dep_map.update(deps)

        fp_in.close()


    resolved = {}

    for target in sorted(dep_map.keys()):
        deps = resolve_depend(target, dep_map)
        resolved[target] = deps[:-1]

    fp.write('---\n')
    fp.write(
        yaml.dump(
            {
                #'dependencies': dep_map,
                'dependencies': resolved,
            },
            sort_keys=True,
            allow_unicode=True,
        )
    )

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

