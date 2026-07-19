#!/usr/bin/env python3
# file: tools/generate_through_spec.py

import sys
import json
import getopt


def usage():
    print("Usage: generate_through_spec.py -o OUTPUT_FILE schema.json")
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

    # schema.json は位置引数
    if not output_file or not args:
        usage()

    schema_path = args[0]

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    through_models = schema.get("through_models", [])

    if not through_models:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# No through models\n")
        print("[INFO] No through_models found.")
        return

    # ★ 1モデル1ファイルなので、最初の1件だけ出力する
    tm = through_models[0]

    name = tm["name"]
    from_model = tm["from"]
    to_model = tm["to"]

    spec = {
        "name": name,
        "fields": {
            "id": {"type": "AutoField"},
            from_model.lower(): {"type": "ForeignKey"},
            to_model.lower(): {"type": "ForeignKey"}
        }
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    print(f"[OK] Generated spec: {output_file}")


if __name__ == "__main__":
    main()
