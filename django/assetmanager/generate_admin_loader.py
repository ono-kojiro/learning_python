#!/usr/bin/env python3

import sys
import getopt
import yaml
import os


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <model_yaml>...")


def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:", ["help", "version", "output="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(0)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = optarg

    if output is None:
        print("ERROR: -o <output> is required", file=sys.stderr)
        sys.exit(1)

    if not args:
        print("ERROR: model YAML files must be specified", file=sys.stderr)
        sys.exit(1)

    # admin.py を生成
    with open(output, "w", encoding="utf-8") as fp:
        fp.write("# auto-generated admin loader\n")

        for filepath in args:
            with open(filepath, "r", encoding="utf-8") as fp_in:
                data = yaml.safe_load(fp_in)

            model = data["name"]
            model_lower = model.lower()

            # admin/<model>_admin.py を import
            fp.write(f"from .admin.{model_lower}_admin import *\n")


if __name__ == "__main__":
    main()
