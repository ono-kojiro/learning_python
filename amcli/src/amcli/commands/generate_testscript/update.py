import os
import json

# VERBOSE が "0" 以外なら DEBUG 有効
DEBUG = os.environ.get("VERBOSE", "0") != "0"

HEADER = """#!/bin/sh

. ./.env

echo "Using BASE_URL=$BASE_URL"
echo
"""

# TAP のテスト件数を先頭に出力
def tap_header(json_files):
    count = len(json_files)
    return f"echo \"1..{count}\"\n\n"


TEMPLATE = """
echo "=== Updating {model} from {jsonfile} ==="

body=$(cat "{jsonfile}")

# id を削除
body=$(echo "$body" | jq 'del(.id)')

# FK / OneToOne / M2M 埋め込み
{fk_patch}

id=$(cat ".id_{model}")

echo "[DEBUG] PATCH $BASE_URL/api/{model_plural}/$id/"
res=$(curl -s -k \
  -X PATCH "$BASE_URL/api/{model_plural}/$id/" \
  -H "Content-Type: application/json" \
  -d "$body")

echo "[DEBUG] response:"
echo "$res"

# TAP 出力
if echo "$res" | jq -e .id >/dev/null 2>&1; then
    echo "ok - update {model} succeeded"
else
    echo "not ok - update {model} failed (invalid JSON or missing id)"
fi

echo
"""


def fk_patch_for(model_cap, fields_def):
    patches = []

    for fname, fdef in fields_def.items():
        ftype = fdef["type"]

        # ForeignKey / OneToOneField
        if ftype in ("ForeignKey", "OneToOneField"):
            target = fdef["to"]
            patches.append(
                f'body=$(echo "$body" | jq --arg fk "$(cat .id_{target.lower()})" \'.{fname} = ($fk|tonumber)\')'
            )

        # ManyToManyField
        elif ftype == "ManyToManyField":
            target = fdef["to"]
            patches.append(
                f'body=$(echo "$body" | jq --arg fk "$(cat .id_{target.lower()})" \'.{fname} = [($fk|tonumber)]\')'
            )

    if not patches:
        return "true"

    return "\n".join(patches)


def run_update(outpath, json_files, schema):
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

        fk_patch = fk_patch_for(model_cap, fields_def).replace("{jsonfile}", base)

        script += TEMPLATE.format(
            model=model,
            model_plural=model_plural,
            jsonfile=base,
            fk_patch=fk_patch
        )

        if DEBUG:
            print(f"[DEBUG] update script for {model} ({base}) → schema model = {model_cap}")

    with open(outpath, "w", encoding="utf-8") as f:
        f.write(script)

    os.chmod(outpath, 0o755)

    print(f"Generated update script: {outpath}")
