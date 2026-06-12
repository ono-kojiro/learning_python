#!/usr/bin/env python3
import sys
import yaml
import getopt

def usage():
    print(f"Usage: {sys.argv[0]} -o <output> <yaml files>")
    sys.exit(1)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
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

    with open(output, "w", encoding="utf-8") as fp:
        for yaml_file in args:
            with open(yaml_file, "r", encoding="utf-8") as yf:
                data = yaml.safe_load(yf)

            name = data["name"]
            lower = name.lower()
            fp.write(f"from .{lower}_serializer import {name}Serializer\n")

if __name__ == "__main__":
    main()

