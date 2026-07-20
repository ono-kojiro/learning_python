# file: /src/amcli/commands/generate_model/modelgen.py

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

    # ★ 既存フィールド名（衝突回避用）
    existing_field_names = set(fields.keys())

    for fname, field_def in fields.items():

        # ★ アンダースコアで始まるキーを除外する
        field_def = {k: v for k, v in field_def.items() if not k.startswith("_")}

        # ★ through_models に含まれている「from→to」の逆側 M2M は生成しない
        skip_m2m = False
        through_models = data.get("through_models", [])
        for tm in through_models:
            if name == tm["to"] and fname == tm["from"].lower() + "s":
                skip_m2m = True
                break

        if skip_m2m:
            continue

        ftype = normalize_field_type(field_def["type"])

        # ---------------------------------------------------------
        # ForeignKey → related_name を自動付与（衝突回避）
        # ---------------------------------------------------------
        if ftype == FieldType.FOREIGN_KEY:

            # 子モデル名の複数形（例: Comment → comments）
            base_related_name = f"{name.lower()}s"

            # 衝突回避：既存フィールド名と同じなら suffix を付ける
            related_name = (
                base_related_name
                if base_related_name not in existing_field_names
                else f"{base_related_name}_set"
            )

            field_def = dict(field_def)
            field_def["related_name"] = related_name

            field_lines.append(
                render_relation_field(fname, field_def, FieldType.FOREIGN_KEY)
            )

        # ---------------------------------------------------------
        # OneToOne → 親側のみ生成
        # ---------------------------------------------------------
        elif ftype == FieldType.ONE_TO_ONE:
            child = field_def["to"]
            is_parent_side = child in compositions.get(name, [])
            if is_parent_side:

                base_related_name = f"{name.lower()}s"
                related_name = (
                    base_related_name
                    if base_related_name not in existing_field_names
                    else f"{base_related_name}_set"
                )

                field_def = dict(field_def)
                field_def["related_name"] = related_name

                field_lines.append(
                    render_relation_field(fname, field_def, FieldType.ONE_TO_ONE)
                )
            else:
                continue

        # ---------------------------------------------------------
        # ManyToMany
        # ---------------------------------------------------------
        elif ftype == FieldType.MANY_TO_MANY:
            field_lines.append(render_many_to_many_field(fname, field_def, name))

        # ---------------------------------------------------------
        # 通常フィールド（JSONField は生成しない）
        # ---------------------------------------------------------
        else:
            # ★ PK 判定：*_id かつ unique=True → primary_key=True に強制
            if fname.endswith("_id") and field_def.get("unique", False):
                field_def = dict(field_def)
                field_def["primary_key"] = True
                field_def.pop("unique", None)

            # ★ JSONField は生成しない（OneToMany は逆参照で表現する）
            if field_def["type"] == "json":
                continue

            field_lines.append(render_simple_field(fname, field_def))

    # __str__() の生成
    str_method = generate_str_method(list(fields.keys()))

    # Meta の生成
    meta_lines = []
    if "meta" in data:
        for k, v in data["meta"].items():
            meta_lines.append(f"{k} = {repr(v)}")

    return field_lines, str_method, meta_lines

# End of file
