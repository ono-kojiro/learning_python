# src/amcli/commands/generate_schema/schema_builder.py

from .primary_key import collect_primary_keys

def build_schema(
    project,
    application,
    models,
    compositions,
    composition_root,
    dependencies,
    all_dependencies,
    reverse_dependencies,
    load_order,
    field_categories,
    general_categories,
    dependency_categories,
    nested,
    inline_order,
    through_models=None,
):
    # ★ 追加：primary_keys を抽出（models は変更しない）
    primary_keys = collect_primary_keys(models)

    device_children = nested.get("Device", [])
    admin_order = {"Device": []}
    for item in device_children:
        model = item.get("model")
        if model:
            admin_order["Device"].append(model)

    normal_admin_models = [m for m in models.keys() if m not in inline_order]


    schema = {
        "project": project,
        "application": application,
        "compositions": compositions,
        "composition_root": composition_root,
        "models": models,  # ← 入力データをそのまま保持
        "primary_keys": primary_keys,  # ★ 追加        
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

    # ★ 追加：through_models を schema.json に含める
    if through_models is not None:
        schema["through_models"] = through_models

    return schema


