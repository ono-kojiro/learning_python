import os
import json

DEBUG = True

HEADER = """#!/bin/sh

. ./.env

echo "Using BASE_URL=$BASE_URL"
echo "Using CERTFILE=$CERTFILE"
echo
"""

TEMPLATE = """
echo "=== Deleting {model} from {jsonfile} ==="

body=$(cat "{jsonfile}")

# *_id を抽出（Python が埋め込むので安全）
value=$(echo "$body" | jq -r ".{key}")

echo "Lookup: {key}=$value"

# 内部 PK を検索
list=$(curl -s -k --cert "$CERTFILE" \
    "$BASE_URL/api/{model_plural}/?{key}=$value")

id=$(echo "$list" | jq -r '.[0].id')

echo "Deleting {model} id=$id"

res=$(curl -s -k --cert "$CERTFILE" \
    -X DELETE "$BASE_URL/api/{model_plural}/$id/")

echo "$res"
echo
"""


def run_delete(outpath, json_files, schema):

    script = HEADER

    model_map = { key.lower(): key for key in schema["models"].keys() }

    for jf in json_files:
        base = os.path.basename(jf)
        model = base.split("_", 1)[1].replace(".json", "")

        if model not in model_map:
            raise ValueError(f"Model '{model}' not found in schema.json")

        model_plural = model + "s"
        key = f"{model}_id"

        script += TEMPLATE.format(
            model=model,
            model_plural=model_plural,
            jsonfile=base,
            key=key
        )

        if DEBUG:
            print(f"[DEBUG] delete script for {model} ({base})")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(script)

    os.chmod(outpath, 0o755)

    print(f"Generated delete script: {outpath}")
