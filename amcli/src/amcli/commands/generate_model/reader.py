import json
from pathlib import Path


def read_json(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return json.load(fp)


def load_compositions():
    schema_path = Path("../work/schema/schema.json")
    if not schema_path.exists():
        return {}

    with open(schema_path, "r", encoding="utf-8") as fp:
        schema = json.load(fp)

    return schema.get("compositions", {})

