#!/usr/bin/env python3

import os
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

def topo_sort(depend_map):
    visited = set()
    order = []

    def visit(model):
        if model in visited:
            return
        visited.add(model)
        for parent in depend_map.get(model, []):
            visit(parent)
        order.append(model)

    for model in depend_map.keys():
        visit(model)

    return order

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
    depend_yaml = None

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
            depend_yaml = optarg
        else:
            assert False, "unknown option"

    print(sys.argv)

    if depend_yaml is None:
        print('ERROR: no depend option', file=sys.stderr)
        ret += 1

    if ret != 0:
        sys.exit(ret)

    depend_map = read_yaml(depend_yaml)["dependencies"]
    # トポロジカルソート（依存関係順）
    order = topo_sort(depend_map)

    module_map = {}

    for filepath in args:

        filename = os.path.basename(filepath)
        if filename == '__init__.py' :
            continue

        module = re.sub(r'\.py$', '', filename)

        fp_in = open(filepath, mode="r", encoding="utf-8")
        while 1:
            line = fp_in.readline()
            if not line:
                break

            line = re.sub(r'\r?\n?$', '', line)
            m = re.search(r'^class\s+(\w+)', line)
            if m :
                cls = m.group(1)
                if cls.endswith("Serializer"):
                    model = re.sub(r'Serializer$', '', cls)
                else :
                    model = cls
                module_map[model] = (module, cls)

        fp_in.close()
    
    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    for model in order:
        if model in module_map:
            module, cls = module_map[model]
            fp.write(f"from .{module} import {cls}\n")

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

