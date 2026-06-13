#!/usr/bin/env python3

import sys
import getopt
import yaml


def usage():
    print(f"Usage: {sys.argv[0]} [-o category.yaml] template/app/*_ref.yaml")


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ------------------------------------------------------------
# すべての *_ref.yaml を読み込み、逆参照情報を構築する
# ------------------------------------------------------------
def load_all_entities(paths):
    entities = {}  # { "NetIF": {...}, "IPv4": {...}, ... }

    for path in paths:
        data = read_yaml(path)

        # ref YAML は name: NetIF の形式
        if "name" not in data or "fields" not in data:
            print(f"{path}: invalid format")
            continue

        name = data["name"]
        entities[name] = data

    return entities


# ------------------------------------------------------------
# カテゴリ判定ロジック（構造ベース + 逆参照）
# ------------------------------------------------------------
def categorize_entity(entity_name, entities):
    data = entities[entity_name]
    fields = data.get("fields", {})

    # ------------------------------------------------------------
    # Owner 判定（ManyToMany / *_ids）
    # ------------------------------------------------------------
    for fdef in fields.values():
        if fdef.get("type") == "ManyToManyField":
            return "owner"

    for fname in fields.keys():
        if fname.endswith("_ids"):
            return "owner"

    # ------------------------------------------------------------
    # 子を持つかどうか（OneToOne / OneToMany の親側）
    # ------------------------------------------------------------
    has_children = False
    for other_name, other_data in entities.items():
        if other_name == entity_name:
            continue

        other_fields = other_data.get("fields", {})
        for fdef in other_fields.values():
            if fdef.get("to") == entity_name:
                if fdef.get("type") in ("OneToOneField", "OneToMany"):
                    has_children = True

    # ------------------------------------------------------------
    # 親への OneToOneField / ForeignKey を持つか（自分の YAML 内）
    # ------------------------------------------------------------
    has_one_to_one_parent = any(
        fdef.get("type") == "OneToOneField"
        for fdef in fields.values()
    )

    has_foreign_key_parent = any(
        fdef.get("type") == "ForeignKey"
        for fdef in fields.values()
    )

    # ------------------------------------------------------------
    # Attribute 判定（親が OneToOne で、子を持たない）
    # ------------------------------------------------------------
    if has_one_to_one_parent and not has_children:
        return "attribute"

    # ------------------------------------------------------------
    # Resource 判定（親が ForeignKey で、子を持つ）
    # ------------------------------------------------------------
    if has_foreign_key_parent and has_children:
        return "resource"

    # ------------------------------------------------------------
    # Resource（デフォルト）
    # ------------------------------------------------------------
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
            print("categorize_entity.py version 3.1")
            sys.exit(0)
        elif opt in ("-o", "--output"):
            output_path = val

    if not args:
        print("ERROR: no input YAML files", file=sys.stderr)
        usage()
        sys.exit(1)

    # すべての *_ref.yaml を読み込む
    entities = load_all_entities(args)

    results = {}

    # 各 Entity を分類
    for entity_name in entities.keys():
        category = categorize_entity(entity_name, entities)
        results[entity_name] = category
        print(f"{entity_name}: {category}")

    # -o で category.yaml に保存
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fp:
            fp.write("---\n")
            yaml.dump({"categories": results}, fp, allow_unicode=True)
        print(f"\nSaved categories to {output_path}")


if __name__ == "__main__":
    main()
