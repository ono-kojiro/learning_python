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

echo "Using BASE_URL=$BASE_URL"
echo
"""

# TAP のテスト件数を先頭に出力
def tap_header(json_files):
    count = len(json_files)
    return f"echo \"1..{count}\"\n\n"


TEMPLATE = """
echo "=== Registering {model} from {jsonfile} ==="
echo "[DEBUG] pwd({model}) = $(pwd)"

# FK / OneToOne / M2M 埋め込み
{fk_patch}

echo "[DEBUG] after jq {model} JSON:"
cat {jsonfile}

# POST 実行
res=$(curl -s -k \
  -X POST "${{BASE_URL}}/api/{model_plural}/" \
  -H "Content-Type: application/json" \
  -d @"{jsonfile}")

echo "[DEBUG] POST response:"
echo "$res"

# ID 抽出
id=$(echo "$res" | jq -r '.id')

# TAP 出力
if [ "$id" = "null" ] || [ -z "$id" ]; then
    echo "not ok - add {model} failed (id not found)"
else
    echo "ok - add {model} succeeded"
    echo "{model} ID = $id"
    echo "$id" > ".id_{model}"
fi

echo
"""


def fk_patch_for(model_cap, fields_def, jsonfile):
    patches = []

    for fname, fdef in fields_def.items():
        ftype = fdef["type"]

        # ForeignKey / OneToOneField
        if ftype in ("ForeignKey", "OneToOneField"):
            target = fdef["to"].lower()
            json_fk_field = f"{fname}_id"

            patches.append(
                f'jq --arg fk "$(cat .id_{target})" \'.{json_fk_field} = ($fk|tonumber)\' "{jsonfile}" > "{jsonfile}.tmp"'
            )
            patches.append(f'mv "{jsonfile}.tmp" "{jsonfile}"')

        # ManyToManyField
        elif ftype == "ManyToManyField":
            target = fdef["to"].lower()
            json_fk_field = f"{fname}_ids"

            patches.append(
                f'jq --arg fk "$(cat .id_{target})" \'.{json_fk_field} = [($fk|tonumber)]\' "{jsonfile}" > "{jsonfile}.tmp"'
            )
            patches.append(f'mv "{jsonfile}.tmp" "{jsonfile}"')

    if not patches:
        return "true"

    return "\n".join(patches)


def run_add(outpath, json_files, schema):
    script = HEADER

    # TAP 件数出力
    script += tap_header(json_files)

    # モデル名マッピング（小文字 → 正しいモデル名）
    model_map = { key.lower(): key for key in schema["models"].keys() }

    for jf in json_files:
        base = os.path.basename(jf)

        model = base.split("_", 1)[1].replace(".json", "")

        if model not in model_map:
            raise ValueError(f"Model '{model}' not found in schema.json")

        model_cap = model_map[model]
        model_plural = model + "s"

        fields_def = schema["models"][model_cap]["fields"]

        fk_patch = fk_patch_for(model_cap, fields_def, base)

        script += TEMPLATE.format(
            model=model,
            model_plural=model_plural,
            jsonfile=base,
            fk_patch=fk_patch
        )

        if DEBUG:
            print(f"[DEBUG] add script for {model} ({base}) → schema model = {model_cap}")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(script)

    os.chmod(outpath, 0o755)

    print(f"Generated add script: {outpath}")
