# src/amcli/commands/generate_schema/general_categories.py

from amcli.utils.constants import FieldType, normalize_field_type

def determine_general_categories(models):
    """
    モデルを entity / attribute / component に一般化する。
    ハードコーディング禁止。
    """

    categories = {}

    for model_name, model_def in models.items():
        fields = model_def["fields"]

        # ManyToMany を持つモデルは entity（Manager, Device）
        if any(
            normalize_field_type(fdef.get("type")) == FieldType.MANY_TO_MANY
            for fdef in fields.values()
        ):
            categories[model_name] = "entity"
            continue

        # JSONField を持つモデルは component（NetIF, IPv4）
        if any(
            normalize_field_type(fdef.get("type")) == FieldType.JSON
            for fdef in fields.values()
        ):
            categories[model_name] = "component"
            continue

        # ForeignKey / OneToOneField を持つモデルは attribute（OS, Comment, Remark）
        if any(
            normalize_field_type(fdef.get("type")) in (FieldType.FOREIGN_KEY, FieldType.ONE_TO_ONE)
            for fdef in fields.values()
        ):
            categories[model_name] = "attribute"
            continue

        # デフォルトは entity
        categories[model_name] = "entity"

    return categories
