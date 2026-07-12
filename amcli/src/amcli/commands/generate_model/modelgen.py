from amcli.utils.constants import FieldType, normalize_field_type
from .reader import load_compositions
from .fields import (
    render_simple_field,
    render_relation_field,
    render_many_to_many_field,
)
from .strgen import generate_str_method


def generate_model_lines(data):
    name = data["name"]
    fields = data["fields"]

    compositions = load_compositions()

    field_lines = []

    for fname, field_def in fields.items():

        # ★ アンダースコアで始まるキーを除外する（ここが重要）
        field_def = {k: v for k, v in field_def.items() if not k.startswith("_")}

        ftype = normalize_field_type(field_def["type"])

        if ftype == FieldType.FOREIGN_KEY:
            field_lines.append(render_relation_field(fname, field_def, FieldType.FOREIGN_KEY))

        elif ftype == FieldType.ONE_TO_ONE:
            child = field_def["to"]
            is_parent_side = child in compositions.get(name, [])
            if is_parent_side:
                field_lines.append(render_relation_field(fname, field_def, FieldType.ONE_TO_ONE))
            else:
                continue

        elif ftype == FieldType.MANY_TO_MANY:
            field_lines.append(render_many_to_many_field(fname, field_def, name))

        else:
            # ★ PK 判定：*_id かつ unique=True → primary_key=True に強制
            if fname.endswith("_id") and field_def.get("unique", False):
                field_def = dict(field_def)  # コピー
                field_def["primary_key"] = True
                field_def.pop("unique", None)  # unique は不要

            field_lines.append(render_simple_field(fname, field_def))

    str_method = generate_str_method(list(fields.keys()))

    meta_lines = []
    if "meta" in data:
        for k, v in data["meta"].items():
            meta_lines.append(f"{k} = {repr(v)}")

    return field_lines, str_method, meta_lines

