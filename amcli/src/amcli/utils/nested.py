# amcli/utils/nested.py

from amcli.utils.constants import FieldType, normalize_field_type


def collect_nested(models):
    """
    モデルの逆参照から nested 構造を構築する。
    ForeignKey → one_to_many
    OneToOneField → one_to_one
    ManyToManyField → many_to_many
    """
    nested = {}

    # 逆参照テーブルを構築
    reverse = {m: [] for m in models}

    for model, data in models.items():
        for fname, fdef in data["fields"].items():
            ftype = normalize_field_type(fdef.get("type"))
            to = fdef.get("to")

            if ftype in (
                FieldType.FOREIGN_KEY,
                FieldType.ONE_TO_ONE,
                FieldType.MANY_TO_MANY,
            ) and to:
                reverse[to].append((model, fname, ftype))

    # nested 構造を構築
    for parent, refs in reverse.items():
        nested_list = []

        for child, fname, ftype in refs:

            if ftype == FieldType.FOREIGN_KEY:
                nested_list.append({
                    "name": child.lower() + "s",
                    "kind": "one_to_many",
                    "model": child,
                    "fk": parent.lower(),
                })

            elif ftype == FieldType.ONE_TO_ONE:
                nested_list.append({
                    "name": child.lower(),
                    "kind": "one_to_one",
                    "model": child,
                    "fk": parent.lower(),
                })

            elif ftype == FieldType.MANY_TO_MANY:
                nested_list.append({
                    "name": child.lower() + "s",
                    "kind": "many_to_many",
                })

        if nested_list:
            nested[parent] = nested_list

    return nested
