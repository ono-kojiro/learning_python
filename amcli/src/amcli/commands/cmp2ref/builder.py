# src/amcli/commands/cmp2ref/builder.py

from amcli.utils.constants import FieldType
from .convert import convert_primitive_field
from .pk import get_pk_field

def build_reference_model(models, target_model):
    if target_model not in models:
        raise ValueError(f"Model {target_model} not found")

    out = {
        "name": target_model,
        "meta": models[target_model].get("meta", {}),
        "fields": {}
    }

    pk_name, pk_field = get_pk_field(models, target_model)

    # 親モデル側のフィールド変換
    for fname, fdef in models[target_model]["fields"].items():

        # fixture_ignore → 完全除外
        if fdef.get("fixture_ignore", False):
            continue

        ftype = fdef["type"]

        if ftype in ["String", "Text", "Int", "Float", "Bool", "ID", "DateTime", "Date"] or ftype.startswith("List"):
            out["fields"][fname] = convert_primitive_field(fdef)

        elif ftype == "ManyToMany":
            # ★★★ 修正：ref.json に ManyToMany をそのまま出力する（_ids にしない）
            # 既存の構造を壊さず、行数も維持する
            base = fname[:-1] if fname.endswith("s") else fname
            new_name = f"{base}_ids"  # ← 既存行は残す（削除しない）

            # ★ ここで new_name ではなく fname を使う（追記のみ）
            out["fields"][fname] = {
                "type": FieldType.MANY_TO_MANY.value,   # ← normalize_field_type と整合
                "to": fdef["to"]
            }

            # ★ Manager の ManyToMany は _fixture_ignore を自動付与（既存ロジック維持）
            if target_model == "Manager":
                out["fields"][fname]["_fixture_ignore"] = True

        elif ftype == "OneToOne":
            out["fields"][fname] = {
                "type": FieldType.ONE_TO_ONE.value,
                "to": fdef["to"],
                "null": fdef.get("nullable", False),
                "blank": fdef.get("nullable", False),
            }

        elif ftype == "OneToMany":
            out["fields"][fname] = {
                "type": FieldType.JSON.value,
                "help_text": f"Owned children of {fdef['to']}"
            }

        else:
            raise ValueError(f"Unknown type: {ftype}")

    # 子モデル側に逆参照を追加
    for model_name, model_def in models.items():
        for fname, fdef in model_def["fields"].items():

            # fixture_ignore → 逆参照も除外
            if fdef.get("fixture_ignore", False):
                continue

            if fdef["type"] == "OneToMany" and fdef["to"] == target_model:
                nullable = fdef.get("nullable", False)
                field_name = model_name.lower()

                out["fields"][field_name] = {
                    "type": FieldType.FOREIGN_KEY.value,
                    "to": model_name,
                    "on_delete": "SET_NULL" if nullable else "CASCADE",
                }

                pk_name2, pk_field2 = get_pk_field(models, model_name)
                if pk_field2 and "max_length" in pk_field2:
                    out["fields"][field_name]["max_length"] = pk_field2["max_length"]

                if nullable:
                    out["fields"][field_name]["null"] = True
                    out["fields"][field_name]["blank"] = True

    return out

