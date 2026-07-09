# amcli/commands/generate_schema.py

from pathlib import Path
import json

from amcli.utils.models import collect_models
from amcli.utils.dependencies import (
    collect_dependencies,
    collect_all_dependencies,
    build_reverse_dependencies,
    topo_sort,
)
from amcli.utils.categories import (
    collect_field_categories,
    categorize_general,
    categorize_dependency,
)
from amcli.utils.nested import collect_nested


# ============================================================
# ★ 依存カテゴリ決定ロジック
# ============================================================
def determine_dependency_categories(models, reverse_dependencies):
    dependency_categories = {}

    for model_name, model_def in models.items():
        fields = model_def["fields"]

        fk_fields = [
            fname for fname, fdef in fields.items()
            if fdef["type"] in ("ForeignKey", "OneToOneField")
        ]
        if fk_fields:
            dependency_categories[model_name] = "fk_child"
            continue

        if reverse_dependencies.get(model_name):
            dependency_categories[model_name] = "fk_parent"
            continue

        dependency_categories[model_name] = categorize_dependency(model_name, models)

    return dependency_categories


# ============================================================
# ★ Inline の階層順ソート（最終版）
# ============================================================
def topo_sort_inline(nested):
    """
    nested は list ベースの構造：
    {
        "Device": [
            {"name": "netifs", "model": "NetIF"},
            {"name": "os", "model": "OS"},
        ],
        "NetIF": [
            {"name": "ipv4s", "model": "IPv4"}
        ],
        ...
    }

    Device を root として DFS を行い、
    子 → 親の順で並べた order をそのまま返す。
    """

    graph = {}

    for parent, children in nested.items():
        graph[parent] = []
        for item in children:
            model = item.get("model")
            if model:
                graph[parent].append(model)

    visited = set()
    order = []

    def dfs(model):
        if model in visited:
            return
        visited.add(model)
        for child in graph.get(model, []):
            dfs(child)
        order.append(model)

    # Device を root として DFS
    dfs("Device")

    # ★ reversed(order) は不要（order がすでに子 → 親）
    return order


# ============================================================
# ★ メイン処理
# ============================================================
def run(output_file, input_files, application=None, project=None):
    ref_paths = [Path(f).resolve() for f in input_files]

    models = collect_models(ref_paths)

    dependencies = collect_dependencies(models)
    all_dependencies = collect_all_dependencies(dependencies)
    reverse_dependencies = build_reverse_dependencies(dependencies)
    load_order = topo_sort(dependencies)

    if "Device" in load_order:
        load_order = ["Device"] + [m for m in load_order if m != "Device"]

    field_categories = collect_field_categories(models)
    general_categories = {m: categorize_general(m, models) for m in models}
    dependency_categories = determine_dependency_categories(models, reverse_dependencies)

    nested = collect_nested(models)

    # ============================================================
    # ★ inline_order（最終版）
    # ============================================================
    inline_order = topo_sort_inline(nested)

    # ============================================================
    # ★ DeviceAdmin の Inline 順（dict/list 両対応）
    # ============================================================
    device_children = nested.get("Device", [])

    admin_order = {
        "Device": []
    }

    for item in device_children:
        model = item.get("model")
        if model:
            admin_order["Device"].append(model)

    # ============================================================
    # ★ schema.json の構築
    # ============================================================
    schema = {
        "project": project,
        "application": application,
        "models": models,
        "dependencies": dependencies,
        "all_dependencies": all_dependencies,
        "reverse_dependencies": reverse_dependencies,
        "load_order": load_order,
        "field_categories": field_categories,
        "general_categories": general_categories,
        "dependency_categories": dependency_categories,
        "nested": nested,
        "inline_order": inline_order,
        "admin_order": admin_order,
    }

    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated schema: {output_path}")
