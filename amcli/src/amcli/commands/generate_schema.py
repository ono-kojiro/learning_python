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


def run(output_file, input_files, application=None, project=None):
    """
    ref.json 群を読み込み、schema.json を生成する。
    解析ロジックはすべて utils に分離されているため、
    この関数は「組み立てるだけ」の責務に限定されている。
    """
    ref_paths = [Path(f).resolve() for f in input_files]

    # --- モデル解析 ---
    models = collect_models(ref_paths)

    # --- 依存関係 ---
    dependencies = collect_dependencies(models)
    all_dependencies = collect_all_dependencies(dependencies)
    reverse_dependencies = build_reverse_dependencies(dependencies)
    load_order = topo_sort(dependencies)

    # Device を先頭にする（あなたの特別ルール）
    if "Device" in load_order:
        load_order = ["Device"] + [m for m in load_order if m != "Device"]

    # --- カテゴリ分類 ---
    field_categories = collect_field_categories(models)
    general_categories = {
        m: categorize_general(m, models) for m in models
    }
    dependency_categories = {
        m: categorize_dependency(m, models) for m in models
    }

    # --- nested 構造 ---
    nested = collect_nested(models)

    # --- schema.json の構築 ---
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
    }

    # --- 出力 ---
    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated schema: {output_path}")
