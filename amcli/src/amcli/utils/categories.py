# amcli/utils/categories.py

from amcli.utils.constants import FieldType, normalize_field_type


def collect_field_categories(models):
    """
    各フィールドタイプごとに model.field の一覧を作成する。
    """
    categories = {}

    for model, data in models.items():
        for fname, fdef in data["fields"].items():
            ftype = normalize_field_type(fdef.get("type"))
            categories.setdefault(ftype, []).append(f"{model}.{fname}")

    return categories


def categorize_general(entity_name, models):
    """
    GeneralCategory を判定する。
    owner / attribute / resource の 3 種類。
    """
    fields = models[entity_name]["fields"]

    # ManyToManyField → owner
    for fdef in fields.values():
        if normalize_field_type(fdef.get("type")) == FieldType.MANY_TO_MANY:
            return "owner"

    # *_ids → owner
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
                ftype = normalize_field_type(fdef.get("type"))
                if ftype in (FieldType.ONE_TO_ONE,):
                    has_children = True

    # 親への OneToOne / ForeignKey
    has_one_to_one_parent = any(
        normalize_field_type(fdef.get("type")) == FieldType.ONE_TO_ONE
        for fdef in fields.values()
    )
    has_foreign_key_parent = any(
        normalize_field_type(fdef.get("type")) == FieldType.FOREIGN_KEY
        for fdef in fields.values()
    )

    # Attribute
    if has_one_to_one_parent and not has_children:
        return "attribute"

    # Resource
    if has_foreign_key_parent and has_children:
        return "resource"

    return "resource"


def categorize_dependency(entity_name, models):
    """
    DependencyCategory を判定する。
    m2m_owner / m2m_target / fk_parent / fk_child / no_dependency
    """
    fields = models[entity_name]["fields"]

    # ManyToMany の所有側
    for fdef in fields.values():
        if normalize_field_type(fdef.get("type")) == FieldType.MANY_TO_MANY:
            return "m2m_owner"

    # ManyToMany の対象側（逆参照）
    for other_name, other_data in models.items():
        if other_name == entity_name:
            continue
        for fdef in other_data.get("fields", {}).values():
            if normalize_field_type(fdef.get("type")) == FieldType.MANY_TO_MANY:
                if fdef.get("to") == entity_name:
                    return "m2m_target"

    # ForeignKey の親側（逆参照）
    for other_name, other_data in models.items():
        if other_name == entity_name:
            continue
        for fdef in other_data.get("fields", {}).values():
            if normalize_field_type(fdef.get("type")) == FieldType.FOREIGN_KEY:
                if fdef.get("to") == entity_name:
                    return "fk_parent"

    # ForeignKey の子側
    for fdef in fields.values():
        if normalize_field_type(fdef.get("type")) == FieldType.FOREIGN_KEY:
            return "fk_child"

    return "no_dependency"
