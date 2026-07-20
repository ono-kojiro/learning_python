#!/usr/bin/env python3
# file: tools/generate_inline.py

import sys
import json
import getopt
import re
import os

from amcli.utils.debug import debug


def safe(name):
    return re.sub(r'\W+', '_', name)


HEADER = """import nested_admin
from ..models import (
    {model},
)
"""


def usage():
    print("Usage: generate_inline.py -m MODEL -o OUTPUT_FILE schema.json")
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

    # ★ schema.json のモデル名も小文字化して比較
    normalized_models = {m.lower(): m for m in models.keys()}

    if model_name not in normalized_models:
        print(f"Error: model '{model_name}' not found in schema.json")
        sys.exit(1)

    # ★ 実際のモデル名（大文字含む）を取得
    actual_model_name = normalized_models[model_name]
    py_model = safe(actual_model_name)

    debug(f"[DEBUG] Generating inline for model={actual_model_name}")

    # -----------------------------
    # Inline クラス生成
    # -----------------------------
    content = HEADER.format(model=py_model)
    content += f"""

class {py_model}Inline(nested_admin.NestedStackedInline):
    model = {py_model}
    extra = 0
"""

    # -----------------------------
    # write output
    # -----------------------------
    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(output_file, "w") as fp:
        fp.write(content)

    debug(f"[OK] Generated inline: {output_file}")


if __name__ == "__main__":
    main()
