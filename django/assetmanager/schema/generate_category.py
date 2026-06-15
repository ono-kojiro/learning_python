#!/usr/bin/env python3

import sys
import getopt
import yaml


def usage():
    print(f"Usage: {sys.argv[0]} [-o category.yaml] schema.yaml")


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ------------------------------------------------------------
# GeneralCategory（旧 categorize_entity.py のロジックを忠実に再現）
# ------------------------------------------------------------
def categorize_general(entity_name, models):
    fields = models[entity_name]["fields"]

    # Owner 判定（ManyToMany / *_ids）
    for fdef in fields.values():
        if fdef.get("type") == "ManyToManyField":
            return "owner"

    for fname in fields.keys():
        if fname.endswith("_ids"):
            return "owner"

    # 子を持つかどうか（逆参照）
    has_children = False
    for other_name, other_data in models.items():
        if other_name == entity_name:
            continue
        for fdef in other_data.get("fields", {}).values():
            if fdef.get("to") == entity_name:
                if fdef.get("type") in ("OneToOneField", "OneToMany"):
                    has_children = True

    # 親への OneToOne / ForeignKey
    has_one_to_one_parent = any(
        fdef.get("type") == "OneToOneField"
        for fdef in fields.values()
    )
    has_foreign_key_parent = any(
        fdef.get("type") == "ForeignKey"
        for fdef in fields.values()
    )

    # Attribute
    if has_one_to_one_parent and not has_children:
        return "attribute"

    # Resource
    if has_foreign_key_parent and has_children:
        return "resource"

    return "resource"


# ------------------------------------------------------------
# DependencyCategory（旧 categorize_entity.py のロジックを忠実に再現）
# ------------------------------------------------------------
def categorize_dependency(entity_name, models):
    fields = models[entity_name]["fields"]

    # ManyToMany の所有側
    for fdef in fields.values():
        if fdef.get("type") == "ManyToManyField":
            return "m2m_owner"

    # ManyToMany の対象側（逆参照）
    for other_name, other_data in models.items():
        if other_name == entity_name:
            continue
        for fdef in other_data.get("fields", {}).values():
            if fdef.get("type") == "ManyToManyField" and fdef.get("to") == entity_name:
                return "m2m_target"

    # ForeignKey の親側（逆参照）
    for other_name, other_data in models.items():
        if other_name == entity_name:
            continue
        for fdef in other_data.get("fields", {}).values():
            if fdef.get("type") == "ForeignKey" and fdef.get("to") == entity_name:
                return "fk_parent"

    # ForeignKey の子側
    for fdef in fields.values():
        if fdef.get("type") == "ForeignKey":
            return "fk_child"

    return "no_dependency"


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
            print("categorize_entity.py version (schema edition)")
            sys.exit(0)
        elif opt in ("-o", "--output"):
            output_path = val

    if not args:
        print("ERROR: schema.yaml must be specified", file=sys.stderr)
        usage()
        sys.exit(1)

    schema_path = args[0]
    schema = read_yaml(schema_path)

    models = schema["models"]

    results_general = {}
    results_dependency = {}

    for entity_name in models.keys():
        g = categorize_general(entity_name, models)
        d = categorize_dependency(entity_name, models)

        results_general[entity_name] = g
        results_dependency[entity_name] = d

        print(f"{entity_name}: general={g}, dependency={d}")

    if output_path:
        with open(output_path, "w", encoding="utf-8") as fp:
            fp.write("---\n")
            yaml.dump(
                {
                    "general_categories": results_general,
                    "dependency_categories": results_dependency,
                },
                fp,
                allow_unicode=True,
            )
        print(f"\nSaved categories to {output_path}")


if __name__ == "__main__":
    main()

