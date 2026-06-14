#!/usr/bin/env python3

import sys
import getopt
import yaml
import os

def usage():
    print(f"Usage: {sys.argv[0]} -o <output> <model_yaml>...")

def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
    except getopt.GetoptError as e:
        print(str(e), file=sys.stderr)
        usage()
        sys.exit(1)

    output = None

    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-o", "--output"):
            output = val

    if output is None:
        print("ERROR: -o <output> is required", file=sys.stderr)
        sys.exit(1)

    if not args:
        print("ERROR: model YAML files must be specified", file=sys.stderr)
        sys.exit(1)

    # 出力ファイルを開く
    with open(output, "w", encoding="utf-8") as fp:
        for yaml_path in args:
            data = read_yaml(yaml_path)
            class_name = data["name"]  # 正しいクラス名
            base = os.path.basename(yaml_path).replace("_ref.yaml", "")
            module = f"{base}_model"

            fp.write(f"from .{module} import {class_name}\n")

if __name__ == "__main__":
    main()
