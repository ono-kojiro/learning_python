#!/usr/bin/env python3

import sys
import getopt
import yaml


def usage():
    print(f"Usage: {sys.argv[0]} [-o category.yaml] <entity_cmp.yaml> ...")


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ------------------------------------------------------------
# カテゴリ判定ロジック
# ------------------------------------------------------------
def categorize_entity(entity_name, data):
    fields = data.get("fields", {})

    # ------------------------------------------------------------
    # Owner 判定（Manager / User / Group など）
    # ------------------------------------------------------------

    # ManyToManyField を持つ → Owner
    for fdef in fields.values():
        if fdef.get("type") == "ManyToManyField":
            return "owner"

    # *_ids を持つ → Owner
    for fname in fields.keys():
        if fname.endswith("_ids"):
            return "owner"

    # ------------------------------------------------------------
    # Attribute 判定（IPv4 など）
    # ------------------------------------------------------------
    for fdef in fields.values():
        if fdef.get("type") in ("OneToOneField", "ForeignKey"):
            if not fdef.get("nullable", True):
                return "attribute"

    # ------------------------------------------------------------
    # Resource 判定（Device, NetIF など）
    # ------------------------------------------------------------
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
        opts, args = getopt.getopt(
            sys.argv[1:], "hvo:", ["help", "version", "output="]
        )
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    output_path = None

    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-v", "--version"):
            print("categorize_entity.py version 1.0")
            sys.exit(0)
        elif opt in ("-o", "--output"):
            output_path = val

    if not args:
        print("ERROR: no input YAML files", file=sys.stderr)
        usage()
        sys.exit(1)

    results = {}

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
        results[entity_name] = category

        # 標準出力にも表示
        print(f"{entity_name}: {category}")

    # -o で category.yaml に保存
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fp:
            fp.write("---\n")  # YAML の開始
            yaml.dump({"categories": results}, fp, allow_unicode=True)
        print(f"\nSaved categories to {output_path}")


if __name__ == "__main__":
    main()
