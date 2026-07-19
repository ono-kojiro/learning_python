from pathlib import Path
import json

from amcli.utils.models import collect_models
from amcli.utils.dependencies import (
    collect_dependencies,
    collect_all_dependencies,
    build_reverse_dependencies,
)
from amcli.utils.categories import collect_field_categories
from amcli.utils.nested import collect_nested

from amcli.utils.compositions import (
    collect_compositions,
    find_composition_root,
    build_load_order_from_compositions,
)

from .general_categories import determine_general_categories
from .inline_order import topo_sort_inline
from .dependency_categories import determine_dependency_categories
from .schema_builder import build_schema

# ★ 追加：through_models を生成するロジック
from .through_model import collect_through_models


def build_reverse_dependencies_detail_mod(models, reverse_dependencies):
    """
    暫定対応：
    reverse_dependencies_detail_mod を生成する。
    ForeignKey の逆参照のみを OneToMany として扱う。
    （親モデル側には付けない）
    """

    print("[DEBUG] === build_reverse_dependencies_detail_mod START ===")

    detail = {}

    # reverse_dependencies は { Parent: [Child1, Child2, ...] }
    for parent, children in reverse_dependencies.items():
        print(f"[DEBUG] Parent={parent}, Children={children}")

        for child in children:
            print(f"[DEBUG]   Checking child={child}")

            fields = models[child]["fields"]
            print(f"[DEBUG]     Fields of {child}: {list(fields.keys())}")

            for fname, fdef in fields.items():
                print(f"[DEBUG]       Field={fname}, type={fdef['type']}, to={fdef.get('to')}")

                # ForeignKey で parent を参照している場合のみ OneToMany
                if fdef["type"] == "ForeignKey" and fdef.get("to") == parent:
                    print(f"[DEBUG]         → MATCH: {child}.{fname} is FK to {parent}")
                    detail[child] = {"type": "OneToMany"}
                else:
                    print(f"[DEBUG]         → SKIP")

    print(f"[DEBUG] === RESULT reverse_dependencies_detail_mod = {detail} ===")
    print("[DEBUG] === build_reverse_dependencies_detail_mod END ===")

    return detail

def run(output_file, input_files, application=None, project=None):
    ref_paths = [Path(f).resolve() for f in input_files]

    # ref/*.json を読み込む
    models = collect_models(ref_paths)

    # ★ 追加：through_models を生成
    through_models = collect_through_models(models)

    compositions = collect_compositions(models)
    composition_root = find_composition_root(compositions)

    dependencies = collect_dependencies(models)
    all_dependencies = collect_all_dependencies(dependencies)
    reverse_dependencies = build_reverse_dependencies(dependencies)

    load_order = build_load_order_from_compositions(compositions, composition_root)

    field_categories = collect_field_categories(models)

    general_categories = determine_general_categories(models)

    dependency_categories = determine_dependency_categories(
        models,
        reverse_dependencies,
        compositions,
        composition_root,
        general_categories,
    )

    nested = collect_nested(models)
    inline_order = topo_sort_inline(nested, composition_root)

    # ★ 追加：through_models を schema に含める
    schema = build_schema(
        project=project,
        application=application,
        models=models,
        compositions=compositions,
        composition_root=composition_root,
        dependencies=dependencies,
        all_dependencies=all_dependencies,
        reverse_dependencies=reverse_dependencies,
        load_order=load_order,
        field_categories=field_categories,
        general_categories=general_categories,
        dependency_categories=dependency_categories,
        nested=nested,
        inline_order=inline_order,
        through_models=through_models,   # ← 追加
    )

    # ★ 暫定対応：reverse_dependencies_detail_mod を生成して schema に追加
    reverse_dependencies_detail_mod = build_reverse_dependencies_detail_mod(models, reverse_dependencies)
    schema["reverse_dependencies_detail_mod"] = reverse_dependencies_detail_mod

    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated schema: {output_path}")
