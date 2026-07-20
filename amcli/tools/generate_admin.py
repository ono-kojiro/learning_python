#!/usr/bin/env python3
# file: tools/generate_admin.py

import sys
import json
import getopt
import re
import os

from amcli.utils.debug import debug


def safe(name):
    return re.sub(r'\W+', '_', name)


HEADER = """import nested_admin
from django.contrib import admin
from ..models import (
    {model},
)
{inline_imports}
"""


def usage():
    print("Usage: generate_admin.py -m MODEL -o OUTPUT_FILE schema.json")
    sys.exit(1)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:o:", ["model=", "output="])
    except getopt.GetoptError:
        usage()

    model_name = None
    output_file = None

    for opt, val in opts:
        if opt in ("-m", "--model"):
            model_name = val.lower()   # ★ 小文字化して保持
        elif opt in ("-o", "--output"):
            output_file = val

    if not model_name or not output_file or not args:
        usage()

    schema_path = args[0]

    with open(schema_path, "r") as f:
        schema = json.load(f)

    models = schema["models"]
    nested = schema["nested"]
    admin_order = schema.get("admin_order", {})
    normal_admin_models = schema.get("normal_admin_models", [])

    # ★ schema.json のモデル名も小文字化して比較
    normalized_models = {m.lower(): m for m in models.keys()}

    if model_name not in normalized_models:
        print(f"Error: model '{model_name}' not found in schema.json")
        sys.exit(1)

    # ★ 実際のモデル名（大文字含む）を取得
    actual_model_name = normalized_models[model_name]
    py_model = safe(actual_model_name)

    debug(f"[DEBUG] Generating admin for model={actual_model_name}")

    # ------------------------------------------------------------
    # Inline の決定
    # ------------------------------------------------------------
    if actual_model_name in admin_order:
        # admin_order に従う
        children = admin_order[actual_model_name]
        debug(f"  admin_order children={children}")
    else:
        # nested の one_to_many / many_to_many を使う
        children = []
        for item in nested.get(actual_model_name, []):
            if item.get("kind") == "one_to_many":
                children.append(item["model"])
            elif item.get("kind") == "many_to_many":
                # ManyToMany は Inline ではなく filter_horizontal が正しい
                pass

        debug(f"  nested children={children}")

    # Inline import の生成
    inline_imports = "\n".join(
        [f"from .{child.lower()}_inline import {safe(child)}Inline" for child in children]
    )

    # Inline ブロック
    inline_block = "\n".join(
        [f"        {safe(child)}Inline," for child in children]
    )

    # ------------------------------------------------------------
    # exclude の生成（nested の name を除外）
    # ------------------------------------------------------------
    exclude_fields = [item["name"] for item in nested.get(actual_model_name, [])]

    # ------------------------------------------------------------
    # Admin クラス生成
    # ------------------------------------------------------------
    if actual_model_name in normal_admin_models:
        # 通常の ModelAdmin
        admin_class = f"""
class {py_model}Admin(admin.ModelAdmin):
    pass

admin.site.register({py_model}, {py_model}Admin)
"""
    else:
        # NestedModelAdmin
        admin_class = f"""
class {py_model}Admin(nested_admin.NestedModelAdmin):
    exclude = {exclude_fields}
    inlines = [
{inline_block}
    ]

admin.site.register({py_model}, {py_model}Admin)
"""

    # ------------------------------------------------------------
    # 出力
    # ------------------------------------------------------------
    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_file, "w") as fp:
        fp.write(
            HEADER.format(
                model=py_model,
                inline_imports=inline_imports
            )
        )
        fp.write(admin_class)

    debug(f"[OK] Generated admin: {output_file}")


if __name__ == "__main__":
    main()

