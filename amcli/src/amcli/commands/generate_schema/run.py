# src/amcli/commands/generate_schema/run.py

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


def run(output_file, input_files, application=None, project=None):
    ref_paths = [Path(f).resolve() for f in input_files]

    models = collect_models(ref_paths)

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
    )

    output_path = Path(output_file).resolve()
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated schema: {output_path}")
