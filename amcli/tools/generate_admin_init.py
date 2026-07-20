#!/usr/bin/env python3
# file: tools/generate_admin_init.py

import sys
import json
import getopt
import os

from amcli.utils.debug import debug


def usage():
    print("Usage: generate_admin_init.py -o OUTPUT_FILE schema.json")
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

    if not output_file or not args:
        usage()

    schema_path = args[0]

    with open(schema_path, "r") as f:
        schema = json.load(f)

    models = schema["models"].keys()

    debug("=== DEBUG: models ===")
    debug(models)

    # ----------------------------------------
    # __init__.py に書く import を生成
    # ----------------------------------------
    lines = []

    for model in models:
        model_lower = model.lower()
        admin_file = f"{model_lower}_admin"
        lines.append(f"from .{admin_file} import *")

    content = "\n".join(lines) + "\n"

    # ----------------------------------------
    # write output
    # ----------------------------------------
    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_file, "w") as fp:
        fp.write(content)

    debug(f"[OK] Generated admin init: {output_file}")


if __name__ == "__main__":
    main()
