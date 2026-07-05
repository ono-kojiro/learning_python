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
echo "=== Updating {model} from {jsonfile} ==="

body=$(cat "{jsonfile}")

# id を削除
body=$(echo "$body" | jq 'del(.id)')

# FK / OneToOne / M2M 埋め込み
{fk_patch}

id=$(cat ".id_{model}")

res=$(curl -s -k \
  -X PATCH "${{BASE_URL}}/api/{model_plural}/${{id}}/" \
  -H "Content-Type: application/json" \
  -d "$body")

echo "$res"
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
    """
    update.sh を生成する。
    schema.json の fields_def を使う。
    """

    script = HEADER

    # ★ モデル名マッピング（小文字 → 正しいモデル名）
    model_map = { key.lower(): key for key in schema["models"].keys() }

    for jf in json_files:
        base = os.path.basename(jf)

        # 例: 001_netif.json → "netif"
        model = base.split("_", 1)[1].replace(".json", "")

        # ★ 正しいモデル名に変換
        if model not in model_map:
            raise ValueError(f"Model '{model}' not found in schema.json")

        model_cap = model_map[model]  # "NetIF" など

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
