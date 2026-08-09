#!/usr/bin/env python3
import sys
import getopt
import yaml
import glob
import os

def usage():
    print("Usage: merge_yaml.py -o output.yml spec/opnsense")
    sys.exit(1)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
    except getopt.GetoptError:
        usage()

    output_file = None
    for opt, val in opts:
        if opt in ("-o", "--output"):
            output_file = val

    if output_file is None:
        usage()

    if len(args) != 1:
        usage()

    input_dir = args[0]
    if not os.path.isdir(input_dir):
        print("Directory not found:", input_dir)
        sys.exit(1)

    merged_paths = {}
    merged_components = {}

    # すべての YAML を走査
    for file in glob.glob(os.path.join(input_dir, "**/*.yml"), recursive=True):
        with open(file) as f:
            data = yaml.safe_load(f)

        if not data:
            continue

        # paths のマージ
        if "paths" in data and isinstance(data["paths"], dict):
            for p, v in data["paths"].items():
                merged_paths[p] = v

        # components.schemas のマージ
        if "components" in data and "schemas" in data["components"]:
            for name, schema in data["components"]["schemas"].items():
                merged_components[name] = schema

    # apiKey 認証を追加
    security_schemes = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
        },
        "ApiSecretAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Secret",
        },
    }

    # 出力
    out = {
        "openapi": "3.0.3",
        "info": {
            "title": "opnsense",
            "version": "0.0.1",
        },
        "paths": merged_paths,
        "components": {
            "schemas": merged_components,
            "securitySchemes": security_schemes,
        },
        "security": [
            {"ApiKeyAuth": []},
            {"ApiSecretAuth": []},
        ],
    }

    with open(output_file, "w") as f:
        yaml.dump(out, f, sort_keys=False)

if __name__ == "__main__":
    main()
