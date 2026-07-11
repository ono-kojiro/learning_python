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

    # ★ root を自動判定
    root = find_root(nested)
    dfs(root)

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

    normal_admin_models = [m for m in models.keys() if m not in inline_order]

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
        "normal_admin_models": normal_admin_models,
    }

    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated schema: {output_path}")


# ============================================================
# ★ ルートモデル判定（nested から自動判定）
# ============================================================
def find_root(nested):
    children = set()
    for parent, items in nested.items():
        for item in items:
            model = item.get("model")
            if model:
                children.add(model)

    roots = [m for m in nested.keys() if m not in children]
    return roots[0] if roots else None
