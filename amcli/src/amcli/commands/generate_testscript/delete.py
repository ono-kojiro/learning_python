import os
import json

DEBUG = True

HEADER = """#!/bin/sh

. ./.env

if [ -z "$BASE_URL" ]; then
    echo "ERROR: BASE_URL is not set in .env"
    exit 1
fi

echo "Using BASE_URL=$BASE_URL"
echo
"""

TEMPLATE = r"""
echo "=== Deleting {model} from {jsonfile} ==="

body=$(cat "{jsonfile}")

key="{key}"
value=$(echo "$body" | jq -r --arg k "$key" '.[$k]')

echo "[DEBUG] key=$key"
echo "[DEBUG] value=$value"

# JSON のみ取得（-v を使わない）
echo "[DEBUG] curl GET $BASE_URL/api/{model_plural}/"
raw=$(curl -s -k "$BASE_URL/api/{model_plural}/")

echo "[DEBUG] raw JSON:"
echo "$raw"

# jq が JSON を確実にパースできるようにする
list="$raw"

echo "[DEBUG] parsed JSON:"
echo "$list" | jq .

echo "[DEBUG] jq filter: select(.[$key] == $value)"
id=$(echo "$list" | jq -r --arg k "$key" --arg v "$value" \
    '.[] | select(.[$k] == $v) | .id')

echo "[DEBUG] extracted id=$id"

echo "Deleting {model} id=$id"

res=$(curl -s -k -X DELETE "$BASE_URL/api/{model_plural}/$id/")

echo "[DEBUG] delete response:"
echo "$res"
echo
"""


def run_delete(outpath, json_files, testschema):
    delete_order = testschema.get("delete_order")
    if not delete_order:
        raise ValueError("testschema.json に delete_order がありません")

    if DEBUG:
        print("[DEBUG] delete_order =", delete_order)

    json_map = {
        os.path.basename(jf).split("_", 1)[1].replace(".json", "").lower(): jf
        for jf in json_files
    }

    ordered_json_files = []
    for model in delete_order:
        jf = json_map.get(model)
        if jf:
            ordered_json_files.append(jf)
        else:
            if DEBUG:
                print(f"[DEBUG] model {model} has no json file, skipping")

    script = HEADER

    for jf in ordered_json_files:
        base = os.path.basename(jf)
        model = base.split("_", 1)[1].replace(".json", "")
        model_plural = model + "s"
        key = f"{model}_id"

        if DEBUG:
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

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(script)

    os.chmod(outpath, 0o755)

    print(f"Generated delete script: {outpath}")
