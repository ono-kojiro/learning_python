# amcli/utils/categories.py (NEW LOGIC VERSION)

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
    GeneralCategory を判定する（新ロジック）。
    owner / attribute / resource の 3 種類。

    新ロジックでは ManyToMany を持つモデルを owner とする。
    Device は owner。
    その他は resource。
    """

    fields = models[entity_name]["fields"]

    # ManyToManyField → owner
    for fdef in fields.values():
        if normalize_field_type(fdef.get("type")) == FieldType.MANY_TO_MANY:
            return "owner"

    # Device は owner（composition root）
    if entity_name == "Device":
        return "owner"

    # その他は resource
    return "resource"


def categorize_dependency(entity_name, models):
    """
    DependencyCategory を判定する（新ロジック）。
    m2m_owner / fk_parent / fk_child / no_dependency
    """

    fields = models[entity_name]["fields"]

    # ManyToMany の所有側
    for fdef in fields.values():
        if normalize_field_type(fdef.get("type")) == FieldType.MANY_TO_MANY:
            return "m2m_owner"

    # ForeignKey / OneToOne の子側
    for fdef in fields.values():
        ftype = normalize_field_type(fdef.get("type"))
        if ftype in (FieldType.FOREIGN_KEY, FieldType.ONE_TO_ONE):
            return "fk_child"

    # Device は fk_parent（composition root）
    if entity_name == "Device":
        return "fk_parent"

    return "no_dependency"
