from pathlib import Path
import json
import yaml
from collections import defaultdict, deque


def read_json(path):
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


# ------------------------------------------------------------
# *_ref.json → models セクション
# ------------------------------------------------------------
def collect_models(ref_files):
    models = {}

    for path in ref_files:
        data = read_json(path)
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
# GeneralCategory
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
# DependencyCategory
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
# トポロジカルソート
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


# ------------------------------------------------------------
# nested 構造
# ------------------------------------------------------------
def collect_nested(models):
    nested = {}

    reverse = {m: [] for m in models}
    for model, data in models.items():
        for fname, fdef in data["fields"].items():
            ftype = fdef.get("type")
            to = fdef.get("to")
            if ftype in ("ForeignKey", "OneToOneField", "ManyToManyField") and to:
                reverse[to].append((model, fname, ftype))

    for parent, refs in reverse.items():
        nested_list = []

        for child, fname, ftype in refs:

            if ftype == "ForeignKey":
                nested_list.append({
                    "name": child.lower() + "s",
                    "kind": "one_to_many",
                    "model": child,
                    "fk": parent.lower(),
                })

            elif ftype == "OneToOneField":
                nested_list.append({
                    "name": child.lower(),
                    "kind": "one_to_one",
                    "model": child,
                    "fk": parent.lower(),
                })

            elif ftype == "ManyToManyField":
                nested_list.append({
                    "name": child.lower() + "s",
                    "kind": "many_to_many",
                })

        if nested_list:
            nested[parent] = nested_list

    return nested


# ------------------------------------------------------------
# amcli 用 run()  ← ★ application / project を追加
# ------------------------------------------------------------
def run(output_file, input_files, application=None, project=None):
    ref_paths = [Path(f).resolve() for f in input_files]

    # --- 解析 ---
    models = collect_models(ref_paths)
    dependencies = collect_dependencies(models)
    field_categories = collect_field_categories(models)

    general_categories = {}
    dependency_categories = {}

    for entity_name in models.keys():
        general_categories[entity_name] = categorize_general(entity_name, models)
        dependency_categories[entity_name] = categorize_dependency(entity_name, models)

    reverse_dependencies = {model: [] for model in dependencies}
    for model, parents in dependencies.items():
        for p in parents:
            reverse_dependencies[p].append(model)

    load_order = topo_sort(dependencies)

    if "Device" in load_order:
        load_order = ["Device"] + [m for m in load_order if m != "Device"]

    nested = collect_nested(models)

    # ★ application / project を schema に追加
    schema = {
        "project": project,
        "application": application,
        "models": models,
        "dependencies": dependencies,
        "reverse_dependencies": reverse_dependencies,
        "load_order": load_order,
        "field_categories": field_categories,
        "general_categories": general_categories,
        "dependency_categories": dependency_categories,
        "nested": nested,
    }

    # JSON で出力
    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated schema: {output_path}")
