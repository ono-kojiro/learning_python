# src/amcli/commands/generate_schema/dependency_categories.py

def determine_dependency_categories(models, reverse_dependencies, compositions, composition_root, general_categories):
    dependency_categories = {}

    for model_name, model_def in models.items():
        fields = model_def["fields"]

        # ManyToMany の「逆側」が m2m_owner
        # → Manager が m2m_owner
        # → Device は m2m_owner ではない
        has_m2m = any(fdef["type"] == "ManyToManyField" for fdef in fields.values())
        if has_m2m and model_name != composition_root:
            dependency_categories[model_name] = "m2m_owner"
            continue

        # 他モデルから参照されているなら fk_parent
        if reverse_dependencies.get(model_name):
            dependency_categories[model_name] = "fk_parent"
            continue

        # 他モデルを参照しているなら fk_child
        has_fk = any(fdef["type"] in ("ForeignKey", "OneToOneField") for fdef in fields.values())
        if has_fk:
            dependency_categories[model_name] = "fk_child"
            continue

        # デフォルトは fk_child
        dependency_categories[model_name] = "fk_child"

    return dependency_categories
