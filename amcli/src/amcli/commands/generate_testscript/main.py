# file: src/amcli/commands/generate_testscript/main.py

import os
import json

from .add import run_add
from .get import run_get
from .update import run_update
from .delete import run_delete

def load_schema(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_ref_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run(action, outpath, json_files, schema_path=None):
    """
    gentestscript のメインルーター
    schema.yml と ref JSON を読み込んで add/update/delete に渡す
    """

    # ★ schema.yml と ref JSON を読み込む
    if schema_path is None:
        # デフォルトの schema.yml を使う（Makefile で指定してもよい）
        schema_path = "work/schema.json"

    schema = load_schema(schema_path)

    # ★ action に応じて処理を振り分ける
    if action == "add":
        run_add(outpath, json_files, schema)

    elif action == "get":
        run_get(outpath, json_files)

    elif action == "update":
        run_update(outpath, json_files, schema)

    elif action == "delete":
        # ★ testschema.json を読み込む（dict）
        with open(schema_path, "r", encoding="utf-8") as fp:
            testschema = json.load(fp)

        run_delete(outpath, json_files, testschema)

    else:
        raise ValueError(f"Unknown action: {action}")

# End of file: src/amcli/commands/generate_testscript/main.py
