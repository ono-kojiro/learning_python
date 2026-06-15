#!/usr/bin/env python3

import sys
import yaml
import getopt


def usage():
    print(f"Usage: {sys.argv[0]} -o <output> schema.yaml")
    sys.exit(1)


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "ho:", ["help", "output="]
        )
    except getopt.GetoptError as e:
        print(str(e))
        usage()

    output = None

    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-o", "--output"):
            output = val

    if not output or not args:
        usage()

    schema_path = args[0]
    schema = read_yaml(schema_path)

    models = schema.get("models", {})

    # admin_loader.py を生成
    with open(output, "w", encoding="utf-8") as fp:
        fp.write("# auto-generated admin loader\n")

        for name in models.keys():
            lower = name.lower()
            fp.write(f"from .admin.{lower}_admin import *\n")


if __name__ == "__main__":
    main()
