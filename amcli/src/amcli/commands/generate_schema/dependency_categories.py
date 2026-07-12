# src/amcli/commands/generate_schema/dependency_categories.py

def determine_dependency_categories(models, reverse_dependencies, compositions, composition_root, general_categories):
    dependency_categories = {}

    root_children = set(compositions.get(composition_root, []))

    for model_name, model_def in models.items():
        fields = model_def["fields"]

        has_fk = any(fdef["type"] in ("ForeignKey", "OneToOneField")
                     for fdef in fields.values())
        has_m2m = any(fdef["type"] == "ManyToManyField"
                      for fdef in fields.values())

        category = general_categories[model_name]

        # ① ManyToMany → m2m_owner
        if has_m2m and model_name not in compositions:
            dependency_categories[model_name] = "m2m_owner"
            continue

        # ② attribute → fk_parent
        if category == "attribute":
            dependency_categories[model_name] = "fk_parent"
            continue

        # ③ component → fk_child
        if category == "component":
            dependency_categories[model_name] = "fk_child"
            continue

        # ④ entity の場合
        if category == "entity":
            if has_fk:
                dependency_categories[model_name] = "fk_child"
            else:
                dependency_categories[model_name] = "none"
            continue

        dependency_categories[model_name] = "none"

    return dependency_categories
