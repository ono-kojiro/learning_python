# src/amcli/commands/generate_testscript/delete.py

import os
import json

DEBUG = True

HEADER = """#!/bin/sh

# Load environment variables
. ./.env

if [ -z "$BASE_URL" ]; then
    echo "ERROR: BASE_URL is not set in .env"
    exit 1
fi

if [ -z "$CERTFILE" ]; then
    echo "ERROR: CERTFILE is not set in .env"
    exit 1
fi

echo "Using BASE_URL=$BASE_URL"
echo "Using CERTFILE=$CERTFILE"
echo
"""

TEMPLATE = """
echo "=== Deleting {model} from {jsonfile} ==="

body=$(cat "{jsonfile}")

key="{key}"
value=$(echo "$body" | jq -r --arg k "$key" '.[$k]')

echo "Lookup: $key=$value"

# 全件取得して jq でフィルタ（API のフィルタリングに依存しない）
list=$(curl -s -k --cert "$CERTFILE" \
    "$BASE_URL/api/{model_plural}/")

id=$(echo "$list" | jq -r --arg k "$key" --arg v "$value" \
    '.[] | select(.[$k] == $v) | .id')

echo "Deleting {model} id=$id"

res=$(curl -s -k --cert "$CERTFILE" \
    -X DELETE "$BASE_URL/api/{model_plural}/$id/")

echo "$res"
echo
"""


def run_delete(outpath, json_files, testschema):
    delete_order = testschema.get("delete_order")
    if not delete_order:
        raise ValueError("testschema.json に delete_order がありません")

    if DEBUG:
        print("[DEBUG] delete_order =", delete_order)

    # ---------------------------------------------------------
    # ★ json_files を model 名で引けるようにする（小文字）
    # ---------------------------------------------------------
    json_map = {
        os.path.basename(jf).split("_", 1)[1].replace(".json", "").lower(): jf
        for jf in json_files
    }

    # ---------------------------------------------------------
    # ★ delete_order に従って json_files を並べ替える
    # ---------------------------------------------------------
    ordered_json_files = []
    for model in delete_order:
        jf = json_map.get(model)
        if jf:
            ordered_json_files.append(jf)
        else:
            if DEBUG:
                print(f"[DEBUG] model {model} has no json file, skipping")

    # ---------------------------------------------------------
    # ★ delete.sh を生成
    # ---------------------------------------------------------
    script = HEADER

    for jf in ordered_json_files:
        base = os.path.basename(jf)
        model = base.split("_", 1)[1].replace(".json", "")
        model_plural = model + "s"
        key = f"{model}_id"

        print("[DEBUG] jsonfile =", jf)
        print("[DEBUG] base =", base)
        print("[DEBUG] model =", model)
        print("[DEBUG] key =", key)

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
