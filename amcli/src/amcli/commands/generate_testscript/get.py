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
echo "=== Registering {model} from {jsonfile} ==="

# JSON 読み込み
body=$(cat "{jsonfile}")

# FK 埋め込み
{fk_patch}

# POST 実行
res=$(curl -s -k \
  -X POST "${{BASE_URL}}/api/{model_plural}/" \
  -H "Content-Type: application/json" \
  -d "$body")

echo "$res"

# ID 抽出
id=$(echo "$res" | jq -r '.id')

if [ "$id" = "null" ]; then
    echo "ERROR: {model} registration failed"
    exit 1
fi

echo "{model} ID = $id"
echo "$id" > ".id_{model}"
echo
"""

def fk_patch_for(model):
    """
    モデルごとに FK 埋め込みの shell コードを返す
    """
    if model == "device":
        return "true  # device は FK なし"

    if model == "comment":
        return 'body=$(jq --arg dev "$(cat .id_device)" \'.device = ($dev|tonumber)\' "{jsonfile}")'

    if model == "netif":
        return 'body=$(jq --arg dev "$(cat .id_device)" \'.device_id = ($dev|tonumber)\' "{jsonfile}")'

    if model == "ipv4":
        return 'body=$(jq --arg nid "$(cat .id_netif)" \'.netif_id = ($nid|tonumber)\' "{jsonfile}")'

    if model == "manager":
        return 'body=$(jq --arg dev "$(cat .id_device)" \'.device_ids = [($dev|tonumber)]\' "{jsonfile}")'

    if model == "os":
        return 'body=$(jq --arg dev "$(cat .id_device)" \'.device = ($dev|tonumber)\' "{jsonfile}")'

    if model == "remark":
        return 'body=$(jq --arg dev "$(cat .id_device)" \'.device = ($dev|tonumber)\' "{jsonfile}")'

    return "true"


def run_get(outpath, json_files):
    script = """#!/bin/sh
. ./.env
"""

    for jf in json_files:
        base = os.path.basename(jf)
        model = base.split("_", 1)[1].replace(".json", "")
        model_plural = model + "s"

        script += f"""
id=$(cat .id_{model})
curl -s -k \
  -X GET "${{BASE_URL}}/api/{model_plural}/${{id}}/"
echo
"""

    with open(outpath, "w") as f:
        f.write(script)
    os.chmod(outpath, 0o755)
