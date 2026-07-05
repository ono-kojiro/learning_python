# src/amcli/commands/generate_testschema.py

import json
from pathlib import Path


def run(schema_path, output_path):
    """
    Generate test_schema.json from schema.json.

    - load_order をそのままコピー
    - delete_order は load_order の逆順を小文字化して生成
    """

    schema_file = Path(schema_path)
    if not schema_file.exists():
        raise FileNotFoundError(f"schema.json not found: {schema_path}")

    with open(schema_file, "r", encoding="utf-8") as fp:
        schema = json.load(fp)

    load_order = schema.get("load_order")
    if not load_order:
        raise ValueError("schema.json に load_order がありません")

    # delete_order を生成
    delete_order = [m.lower() for m in reversed(load_order)]

    test_schema = {
        "load_order": load_order,
        "delete_order": delete_order,
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(test_schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated test_schema: {out_file}")

