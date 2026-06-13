#!/usr/bin/env python3

import sys
import getopt
import yaml
import re


def usage():
    print(f"Usage: {sys.argv[0]} <entity_cmp.yaml> ...")


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ------------------------------------------------------------
# カテゴリ判定ロジック
# ------------------------------------------------------------
def categorize_entity(entity_name, data):
    fields = data.get("fields", {})

    # 1. Owner 判定
    # ManyToManyField を持つ → Owner
    for fdef in fields.values():
        if fdef.get("type") == "ManyToManyField":
            return "owner"

    # *_ids を持つ → Owner
    for fname in fields.keys():
        if fname.endswith("_ids"):
            return "owner"

    # 2. Attribute 判定
    # 親への OneToOne / ForeignKey（nullable=false）
    for fdef in fields.values():
        if fdef.get("type") in ("OneToOneField", "ForeignKey"):
            if not fdef.get("nullable", True):
                return "attribute"

    # 3. Resource 判定
    # 固有IDを持つ（xxx_id）
    for fname in fields.keys():
        if fname.endswith("_id"):
            return "resource"

    # デフォルトは resource
    return "resource"


# ------------------------------------------------------------
# main
# ------------------------------------------------------------
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "version"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    for opt, _ in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-v", "--version"):
            print("categorize_entity.py version 1.0")
            sys.exit(0)

    if not args:
        print("ERROR: no input YAML files", file=sys.stderr)
        usage()
        sys.exit(1)

    # 各 YAML を読み込んでカテゴリ判定
    for path in args:
        data = read_yaml(path)

        # YAML のトップレベルキー（Entity 名）を取得
        if len(data.keys()) != 1:
            print(f"{path}: invalid format", file=sys.stderr)
            continue

        entity_name = list(data.keys())[0]
        entity_def = data[entity_name]

        category = categorize_entity(entity_name, entity_def)
        print(f"{entity_name}: {category}")


if __name__ == "__main__":
    main()

