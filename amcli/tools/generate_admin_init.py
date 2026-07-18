#!/usr/bin/env python3
# file: tools/generate_admin_init.py

import sys
import json
import getopt
import re


def safe(name):
    return re.sub(r'\W+', '_', name)


HEADER = """import nested_admin
from django.contrib import admin
from ..models import (
{model_imports}
)
"""


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

    models = schema["models"]
    nested = schema["nested"]
    admin_order = schema.get("admin_order", {})
    normal_admin = schema.get("normal_admin_models", [])

    print("=== DEBUG: nested ===")
    print(json.dumps(nested, indent=2))

    print("=== DEBUG: admin_order ===")
    print(json.dumps(admin_order, indent=2))

    print("=== DEBUG: normal_admin_models ===")
    print(json.dumps(normal_admin, indent=2))

    # -----------------------------
    # import models
    # -----------------------------
    model_imports = "\n".join([f"    {safe(m)}," for m in models.keys()])

    # -----------------------------
    # Inline definitions
    # -----------------------------
    inline_defs = []

    for model in models.keys():
        py_model = safe(model)

        print(f"\n=== DEBUG: Inline for model={model} ===")

        inline_defs.append(
            f"""
class {py_model}Inline(nested_admin.NestedStackedInline):
    model = {py_model}
    extra = 0
"""
        )

    # -----------------------------
    # Admin definitions
    # -----------------------------
    admin_defs = []

    for model in models.keys():
        py_model = safe(model)

        print(f"\n=== DEBUG: Admin for model={model} ===")

        # DeviceAdmin の inline は admin_order に従う
        if model in admin_order:
            children = admin_order[model]
            print(f"  admin_order children={children}")
        else:
            # nested のうち one_to_many のみ採用
            children = [
                item["model"]
                for item in nested.get(model, [])
                if item.get("kind") == "one_to_many"
            ]
            print(f"  nested one_to_many children={children}")

        # exclude の生成（many_to_many + one_to_many 全て）
        exclude_fields = [
            item["name"]
            for item in nested.get(model, [])
        ]
        print(f"  exclude_fields={exclude_fields}")

        child_inline_list = [
            f"        {safe(child)}Inline,"
            for child in children
        ]

        inlines_block = "\n".join(child_inline_list)

        # Manager は normal_admin_models に従う
        if model in normal_admin:
            print("  → normal_admin_models: using ModelAdmin")
            admin_defs.append(
                f"""
class {py_model}Admin(admin.ModelAdmin):
    pass
admin.site.register({py_model}, {py_model}Admin)
"""
            )
        else:
            admin_defs.append(
                f"""
class {py_model}Admin(nested_admin.NestedModelAdmin):
    exclude = {exclude_fields}
    inlines = [
{inlines_block}
    ]
admin.site.register({py_model}, {py_model}Admin)
"""
            )

    # -----------------------------
    # write output
    # -----------------------------
    with open(output_file, "w") as f:
        f.write(HEADER.format(model_imports=model_imports))
        f.write("\n".join(inline_defs))
        f.write("\n".join(admin_defs))

    print(f"[OK] Generated admin init: {output_file}")


if __name__ == "__main__":
    main()
