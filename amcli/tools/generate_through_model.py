#!/usr/bin/env python3
# file: tools/generate_through_model.py

import sys
import json
import getopt
import re


def safe(name):
    return re.sub(r'\W+', '_', name)


def usage():
    print("Usage: generate_through_model.py -o OUTPUT_FILE schema.json")
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

    through_models = schema.get("through_models", [])

    print("=== DEBUG: through_models ===")
    print(json.dumps(through_models, indent=2))

    if not through_models:
        print("=== DEBUG: no through_models found ===")
        with open(output_file, "w") as f:
            f.write("# No through models\n")
        return

    # ★ through_models が複数あっても対応
    imports = set()
    body = ""

    for tm in through_models:
        from_model = tm["from"]
        to_model = tm["to"]
        name = tm["name"]

        imports.add(f"from .{from_model.lower()}_model import {from_model}")
        imports.add(f"from .{to_model.lower()}_model import {to_model}")

        body += f"""
class {name}(models.Model):
    {from_model.lower()} = models.ForeignKey({from_model}, on_delete=models.CASCADE)
    {to_model.lower()} = models.ForeignKey({to_model}, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("{from_model.lower()}", "{to_model.lower()}")
"""

    header = "from django.db import models\n" + "\n".join(imports) + "\n\n"

    with open(output_file, "w") as f:
        f.write(header)
        f.write(body)

    print(f"[OK] Generated through model: {output_file}")


if __name__ == "__main__":
    main()
