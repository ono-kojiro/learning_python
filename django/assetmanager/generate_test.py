#!/usr/bin/env python3

import sys
import getopt
import yaml
import json
import os
import random
import string

from jinja2 import Environment, FileSystemLoader

def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)
    
def main():
    options, args = getopt.getopt(
        sys.argv[1:], "ho:m:", ["help", "output=", "meta="]
    )

    output_file = None
    meta_path = None

    for opt, val in options:
        if opt in ("-o", "--output"):
            output_file = val
        elif opt in ("-m", "--meta"):
            meta_path = val

    if not meta_path:
        print("ERROR: meta.yaml is required (-m)")
        return

    if not output_file:
        print("ERROR: output file is required (-o)")
        return

    if len(args) != 1:
        print("ERROR: exactly one *_ref.yaml must be specified")
        return

    # meta.yaml 読み込み
    meta = read_yaml(meta_path)
    meta_models = meta["models"]

    # *_ref.yaml 読み込み
    ref_yaml = args[0]
    data = read_yaml(ref_yaml)
    model = data["name"]
    fields = meta_models[model]["fields"]

    # main の中でファイルを開く
    with open(output_file, "w", encoding="utf-8") as fp:

        env = Environment(
            loader=FileSystemLoader("template/tests"),
            autoescape=False
        )

        env.filters["repr"] = repr

        template = env.get_template("test_generated_template.j2")

        content = template.render(
            model=model,
            model_lower=model.lower(),
            fields=fields,
            fields_json=repr(fields)
        )

        fp.write(content + '\n')

    print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
