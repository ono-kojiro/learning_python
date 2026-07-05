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
echo "=== GET {model} ==="

id=$(cat .id_{model})

echo "[DEBUG] GET $BASE_URL/api/{model_plural}/$id/"
res=$(curl -s -k -X GET "$BASE_URL/api/{model_plural}/$id/")

echo "[DEBUG] response:"
echo "$res"

# TAP 出力
if echo "$res" | jq -e .id >/dev/null 2>&1; then
    echo "ok - get {model} succeeded"
else
    echo "not ok - get {model} failed (invalid JSON or missing id)"
fi

echo
"""


def run_get(outpath, json_files):
    script = HEADER

    # TAP 件数出力
    script += tap_header(json_files)

    for jf in json_files:
        base = os.path.basename(jf)
        model = base.split("_", 1)[1].replace(".json", "")
        model_plural = model + "s"

        script += TEMPLATE.format(
            model=model,
            model_plural=model_plural
        )

        if DEBUG:
            print(f"[DEBUG] get script for {model} ({base})")

    with open(outpath, "w") as f:
        f.write(script)

    os.chmod(outpath, 0o755)

    print(f"Generated get script: {outpath}")
