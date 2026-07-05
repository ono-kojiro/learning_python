import os
import json

DEBUG = True

HEADER = """#!/bin/sh

. ./.env

echo "Using BASE_URL=$BASE_URL"
echo "Using CERTFILE=$CERTFILE"
echo

# default
DRY_RUN=0

"""

TEMPLATE = """
echo "=== Deleting {model} from {jsonfile} ==="

body=$(cat "{jsonfile}")

# *_id を抽出（Python が埋め込むので安全）
value=$(echo "$body" | jq -r ".{key}")

echo "Lookup: {key}=$value"

# 内部 PK を検索
list=$(curl -s -k \
    "$BASE_URL/api/{model_plural}/?{key}=$value")

# 配列形式（list API）を試す（jqエラー抑止）
id=$(echo "$list" | jq -r '.[0]? | .id // empty')

# 単一オブジェクト形式を試す
if [ -z "$id" ] || [ "$id" = "null" ]; then
    id=$(echo "$list" | jq -r '.id // empty')
fi

echo "Deleting {model} id=$id"

# ============================
# ★ dry-run オプション対応
# ============================
if [ "$DRY_RUN" = "1" ]; then
    echo "[DRY-RUN] curl -s -k -X DELETE \\"$BASE_URL/api/{model_plural}/$id/\\""
else
    res=$(curl -s -k \
        -X DELETE "$BASE_URL/api/{model_plural}/$id/")
    echo "$res"
fi

echo
"""


def run_delete(outpath, json_files, schema):

    script = HEADER

    # ----------------------------------------
    # ★ schema.json の load_order を逆順にする
    # ----------------------------------------
    load_order = schema.get("load_order")

    if not load_order:
        if DEBUG:
            print("[DEBUG] load_order missing, using json_files order")
        load_order = [
            os.path.basename(jf).split("_", 1)[1].replace(".json", "")
            for jf in json_files
        ]

    # ★ 小文字化して delete_order を作る
    delete_order = [m.lower() for m in reversed(load_order)]

    if DEBUG:
        print("[DEBUG] load_order =", load_order)
        print("[DEBUG] delete_order =", delete_order)

    # json_files を model 名で引けるようにする（小文字）
    json_map = {
        os.path.basename(jf).split("_", 1)[1].replace(".json", "").lower(): jf
        for jf in json_files
    }

    # ----------------------------------------
    # ★ delete_order に従って json_files を並べ替える
    # ----------------------------------------
    ordered_json_files = []
    for model in delete_order:
        jf = json_map.get(model)
        if jf:
            ordered_json_files.append(jf)
        else:
            if DEBUG:
                print(f"[DEBUG] model {model} has no json file, skipping")

    # ----------------------------------------
    # ★ 並べ替えた順序で delete.sh を生成
    # ----------------------------------------
    for jf in ordered_json_files:
        base = os.path.basename(jf)
        model = base.split("_", 1)[1].replace(".json", "")

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
