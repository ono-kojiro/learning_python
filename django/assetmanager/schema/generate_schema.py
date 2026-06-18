#!/usr/bin/env python3

import sys
import getopt
import yaml
from collections import defaultdict, deque


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ------------------------------------------------------------
# *_ref.yaml → models セクション
# ------------------------------------------------------------
def collect_models(ref_files):
    models = {}

    for path in ref_files:
        data = read_yaml(path)
        name = data["name"]
        fields = data.get("fields", {})
        models[name] = {"fields": fields}

    return models


# ------------------------------------------------------------
# 依存関係（ForeignKey / OneToOne / ManyToMany）
# ------------------------------------------------------------
def collect_dependencies(models):
    deps = {m: [] for m in models}

    for model, data in models.items():
        fields = data["fields"]
        for fname, fdef in fields.items():
            ftype = fdef.get("type")
            to = fdef.get("to")

            if ftype in ("ForeignKey", "OneToOneField", "ManyToManyField"):
                if to:
                    deps[model].append(to)

    return deps


# ------------------------------------------------------------
# フィールドカテゴリ分類
# ------------------------------------------------------------
def collect_field_categories(models):
    categories = {}

    for model, data in models.items():
        fields = data["fields"]
        for fname, fdef in fields.items():
            ftype = fdef.get("type", "Unknown")
            categories.setdefault(ftype, []).append(f"{model}.{fname}")

    return categories


# ------------------------------------------------------------
# GeneralCategory（旧 categorize_entity.py のロジック）
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
# DependencyCategory（旧 categorize_entity.py のロジック）
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
# トポロジカルソート（generate_depend.py のロジック）
# ------------------------------------------------------------
def topo_sort(dep_map):
    graph = defaultdict(list)
    indegree = defaultdict(int)

    for model, parents in dep_map.items():
        indegree[model] = len(parents)
        for p in parents:
            graph[p].append(model)

    queue = deque([m for m, d in indegree.items() if d == 0])
    order = []

    while queue:
        m = queue.popleft()
        order.append(m)

        for child in graph[m]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    return order

# --- 追加 ---
def collect_nested(models):
    """
    逆参照からネスト構造を構築する。
    Device → NetIF → IPv4 のような構造を自動検出する。
    """
    nested = {}

    # 逆参照マップを作る
    reverse = {m: [] for m in models}
    for model, data in models.items():
        for fname, fdef in data["fields"].items():
            ftype = fdef.get("type")
            to = fdef.get("to")
            if ftype in ("ForeignKey", "OneToOneField", "ManyToManyField") and to:
                reverse[to].append((model, fname, ftype))

    # 親モデルごとにネスト構造を作る
    for parent, refs in reverse.items():
        nested_list = []

        for child, fname, ftype in refs:

            # OneToMany（ForeignKey の逆参照）
            if ftype == "ForeignKey":
                nested_list.append({
                    "name": child.lower() + "s",
                    "kind": "one_to_many",
                    "model": child,
                    "fk": parent.lower(),
                })

            # OneToOne
            elif ftype == "OneToOneField":
                nested_list.append({
                    "name": child.lower(),
                    "kind": "one_to_one",
                    "model": child,
                    "fk": parent.lower(),
                })

            # ManyToMany
            elif ftype == "ManyToManyField":
                nested_list.append({
                    "name": child.lower() + "s",
                    "kind": "many_to_many",
                })

        if nested_list:
            nested[parent] = nested_list

    return nested

# ------------------------------------------------------------
# main
# ------------------------------------------------------------
def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "ho:", ["help", "output="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = "schema.yaml"

    for opt, val in opts:
        if opt in ("-h", "--help"):
            print("Usage: generate_schema.py -o schema.yaml template/app/*_ref.yaml")
            return
        elif opt in ("-o", "--output"):
            output = val

    if not args:
        print("ERROR: *_ref.yaml files must be specified")
        return

    ref_files = args

    # --- 解析 ---
    models = collect_models(ref_files)
    dependencies = collect_dependencies(models)
    field_categories = collect_field_categories(models)

    # --- GeneralCategory / DependencyCategory ---
    general_categories = {}
    dependency_categories = {}

    for entity_name in models.keys():
        general_categories[entity_name] = categorize_general(entity_name, models)
        dependency_categories[entity_name] = categorize_dependency(entity_name, models)

    # --- reverse_dependencies ---
    reverse_dependencies = {model: [] for model in dependencies}
    for model, parents in dependencies.items():
        for p in parents:
            reverse_dependencies[p].append(model)

    # --- load_order ---
    load_order = topo_sort(dependencies)

    # Device を最優先にする（暫定対応）
    if "Device" in load_order:
        load_order = ["Device"] + [m for m in load_order if m != "Device"]

    # --- ★ nested 構造を追加 ---
    nested = collect_nested(models)

    # --- schema.yaml の構造 ---
    schema = {
        "models": models,
        "dependencies": dependencies,
        "reverse_dependencies": reverse_dependencies,
        "load_order": load_order,
        "field_categories": field_categories,
        "general_categories": general_categories,
        "dependency_categories": dependency_categories,
        "nested": nested,   # ★ 追加
    }

    # --- 出力 ---
    with open(output, "w", encoding="utf-8") as fp:
        fp.write("# Generated by generate_schema.py\n")
        yaml.dump(schema, fp, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    main()
