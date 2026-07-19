# src/amcli/commands/generate_testscript/add.py

import os
import json

DEBUG = os.environ.get("VERBOSE", "0") != "0"

HEADER = """#!/bin/sh

. ./.env

if [ -z "$BASE_URL" ]; then
    echo "ERROR: BASE_URL is not set in .env"
    exit 1
fi

echo "Using BASE_URL=$BASE_URL"
echo
"""

def tap_header(total_tests):
    return f"echo \"1..{total_tests}\"\n\n"


TEMPLATE_MODEL = """
echo "=== Registering {model} from {jsonfile} ==="

res=$(curl -s -k \
  -X POST "${{BASE_URL}}/api/{model_plural}/" \
  -H "Content-Type: application/json" \
  -d @"{jsonfile}")

echo "[DEBUG] POST response:"
echo "$res"

id=$(echo "$res" | jq -r '.id')

if [ "$id" = "null" ] || [ -z "$id" ]; then
    echo "not ok - add {model} failed (id not found)"
else
    echo "ok - add {model} succeeded"
    echo "$id" > ".id_{model}"
fi

echo
"""


# DeviceManager 登録用テンプレート
TEMPLATE_DM = """
echo "=== Registering DeviceManager (device={device}, manager={manager}) ==="

json_dm=$(cat <<EOF
{{
  "device": {device},
  "manager": {manager}
}}
EOF
)

res=$(curl -s -k \
  -X POST "${{BASE_URL}}/api/devicemanager/" \
  -H "Content-Type: application/json" \
  -d "$json_dm")

echo "[DEBUG] POST response:"
echo "$res"

id=$(echo "$res" | jq -r '.id')

if [ "$id" = "null" ] || [ -z "$id" ]; then
    echo "not ok - add devicemanager failed"
else
    echo "ok - add devicemanager succeeded"
fi

echo
"""


def run_add(outpath, json_files, schema):
    script = HEADER

    # Device と Manager の登録数 + DeviceManager の登録数
    total_tests = len(json_files)

    # DeviceManager の登録は Device と Manager の組み合わせ分だけ追加
    # 今は簡易に「Device と Manager が両方存在するなら 1 件追加」
    has_device = any("device" in jf for jf in json_files)
    has_manager = any("manager" in jf for jf in json_files)

    if has_device and has_manager:
        total_tests += 1

    script += tap_header(total_tests)

    model_map = { key.lower(): key for key in schema["models"].keys() }

    # Device と Manager の ID を後で使うため保持
    device_id_var = None
    manager_id_var = None

    for jf in json_files:
        base = os.path.basename(jf)
        model = base.split("_", 1)[1].replace(".json", "")

        if model not in model_map:
            raise ValueError(f"Model '{model}' not found in schema.json")

        model_cap = model_map[model]
        model_plural = model + "s"

        script += TEMPLATE_MODEL.format(
            model=model,
            model_plural=model_plural,
            jsonfile=base
        )

        if model == "device":
            device_id_var = ".id_device"
        if model == "manager":
            manager_id_var = ".id_manager"

    # DeviceManager 登録
    if device_id_var and manager_id_var:
        script += TEMPLATE_DM.format(
            device=f"$(cat {device_id_var})",
            manager=f"$(cat {manager_id_var})"
        )

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(script)

    os.chmod(outpath, 0o755)

    print(f"Generated add script: {outpath}")

