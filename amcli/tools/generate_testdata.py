#!/usr/bin/env python3
# file: tools/generate_testdata.py
#
# Generate ADD-phase testdata JSON for a single model.
# -m MODEL_NAME (case-insensitive; compared in lowercase)
# -o OUTPUT_FILE (explicit file path)
# schema.json is positional argument
#
# tools/generate_through_spec.py と同じ構造・方針

import sys
import json
import getopt
import os
import datetime


def usage():
    print("Usage: generate_testdata.py -m MODEL -o OUTPUT_FILE schema.json")
    sys.exit(1)


# ============================================================
# Utility
# ============================================================

def gen_dummy_value(fname, fdef):
    """Generate dummy values for non-FK fields."""
    ftype = fdef.get("type")

    if ftype == "AutoField":
        return None

    if ftype == "CharField":
        return f"{fname.upper()}-{os.urandom(4).hex()}"

    if ftype == "IntegerField":
        return 1

    if ftype == "DateTimeField":
        return datetime.datetime.now().isoformat()

    if ftype == "JSONField":
        return []   # ★ JSONField は必ずリスト

    return None


# ============================================================
# JSON generator
# ============================================================

def gen_json(model_name, fields_def, output_file):
    """
    Generate JSON for ADD phase:
    - No PK
    - FK → *_id = null
    - OneToOne → null
    - M2M → *_ids = []
    - JSONField → []
    """
    body = {}

    for fname, fdef in fields_def.items():

        # PK は生成しない
        if fname == "id":
            continue

        ftype = fdef["type"]

        # ForeignKey
        if ftype == "ForeignKey":
            body[f"{fname}_id"] = None
            continue

        # OneToOneField
        if ftype == "OneToOneField":
            body[fname] = None
            continue

        # ManyToMany
        if ftype == "ManyToManyField":
            body[f"{fname}_ids"] = []
            continue

        # 通常フィールド
        body[fname] = gen_dummy_value(fname, fdef)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(body, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"[OK] wrote {output_file}")


# ============================================================
# Entry point
# ============================================================

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:o:", ["model=", "output="])
    except getopt.GetoptError:
        usage()

    model_name = None
    output_file = None

    for opt, val in opts:
        if opt in ("-m", "--model"):
            model_name = val.lower()   # ★ 小文字化して比較
        elif opt in ("-o", "--output"):
            output_file = val

    if not model_name or not output_file or not args:
        usage()

    schema_path = args[0]

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    # schema["models"] のキーを小文字化して扱う
    models_lower = {k.lower(): k for k in schema["models"].keys()}

    # through_models も小文字化
    through_lower = {tm["name"].lower() for tm in schema.get("through_models", [])}

    if model_name in through_lower:
        print(f"[ERROR] {model_name} is a through model and cannot be generated.")
        sys.exit(1)

    if model_name not in models_lower:
        print(f"[ERROR] Model not found in schema: {model_name}")
        sys.exit(1)

    # 正規化されたモデル名（大文字の元名）
    model_cap = models_lower[model_name]

    fields_def = schema["models"][model_cap]["fields"]

    gen_json(model_name, fields_def, output_file)


if __name__ == "__main__":
    main()
