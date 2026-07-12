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

    # --- PK は primary_key を付けない（model.mk が付ける） ---
    pk_name, pk_field = get_pk_field(models, target_model)
    # PK フィールドは unique=True のまま扱う

    # ---------------------------------------
    # 親モデル側のフィールド変換
    # ---------------------------------------
    for fname, fdef in models[target_model]["fields"].items():
        ftype = fdef["type"]

        # プリミティブ型
        if ftype in ["String", "Text", "Int", "Float", "Bool", "ID", "DateTime", "Date"] or ftype.startswith("List"):
            out["fields"][fname] = convert_primitive_field(fdef)

        # ManyToMany
        elif ftype == "ManyToMany":
            base = fname[:-1] if fname.endswith("s") else fname
            new_name = f"{base}_ids"
            out["fields"][new_name] = {
                "type": FieldType.MANY_TO_MANY.value,
                "to": fdef["to"]
            }

        # OneToOne
        elif ftype == "OneToOne":
            out["fields"][fname] = {
                "type": FieldType.ONE_TO_ONE.value,
                "to": fdef["to"],
                "null": fdef.get("nullable", False),
                "blank": fdef.get("nullable", False),
            }

        # OneToMany
        elif ftype == "OneToMany":
            out["fields"][fname] = {
                "type": FieldType.JSON.value,
                "help_text": f"Owned children of {fdef['to']}"
            }

        else:
            raise ValueError(f"Unknown type: {ftype}")

    # ---------------------------------------
    # 子モデル側に逆参照を追加
    # ---------------------------------------
    for model_name, model_def in models.items():
        for fname, fdef in model_def["fields"].items():

            # OneToMany → 子側に ForeignKey
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

            # OneToOne → 子側に OneToOneField
            if fdef["type"] == "OneToOne" and fdef["to"] == target_model:
                field_name = model_name.lower()

                out["fields"][field_name] = {
                    "type": FieldType.ONE_TO_ONE.value,
                    "to": model_name,
                    "null": fdef.get("nullable", False),
                    "blank": fdef.get("nullable", False),
                }

    return out

