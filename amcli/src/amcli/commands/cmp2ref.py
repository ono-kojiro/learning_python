from pathlib import Path
import yaml
import json

from amcli.utils.constants import FieldType


def load_owner_models(paths):
    models = {}
    for path in paths:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            models.update(data)
    return models


# ---------------------------------------------------------
# プリミティブ型 → Django フィールド型
# ---------------------------------------------------------
def convert_primitive_field(fdef):
    out = {}
    ftype = fdef["type"]

    if ftype == "String":
        out["type"] = FieldType.CHAR.value
        out["max_length"] = fdef.get("max_length", 255)

    elif ftype == "Text":
        out["type"] = FieldType.TEXT.value

    elif ftype == "Int":
        out["type"] = FieldType.INTEGER.value

    elif ftype == "Float":
        out["type"] = FieldType.FLOAT.value

    elif ftype == "Bool":
        out["type"] = FieldType.BOOLEAN.value

    elif ftype == "ID":
        out["type"] = FieldType.CHAR.value
        out["max_length"] = fdef.get("max_length", 100)
        out["unique"] = True

    elif ftype.startswith("List"):
        out["type"] = FieldType.JSON.value

    elif ftype == "DateTime":
        out["type"] = FieldType.DATETIME.value

    elif ftype == "Date":
        out["type"] = FieldType.DATE.value

    else:
        raise ValueError(f"Unknown primitive type: {ftype}")

    if "unique" in fdef:
        out["unique"] = fdef["unique"]

    if "default" in fdef:
        out["default"] = fdef["default"]

    if "help" in fdef:
        out["help_text"] = fdef["help"]

    return out


# ---------------------------------------------------------
# PK フィールドの抽出
# ---------------------------------------------------------
def get_pk_field(models, model_name):
    fields = models[model_name]["fields"]
    for fname, fdef in fields.items():
        if fdef.get("unique") and fdef["type"] in ["String", "ID"]:
            return fname, convert_primitive_field(fdef)
    return None, None


# ---------------------------------------------------------
# 参照モデル構築
# ---------------------------------------------------------
def build_reference_model(models, target_model):
    if target_model not in models:
        raise ValueError(f"Model {target_model} not found")

    out = {
        "name": target_model,
        "meta": models[target_model].get("meta", {}),
        "fields": {}
    }

    # -------------------------------
    # 自モデルのフィールド変換
    # -------------------------------
    for fname, fdef in models[target_model]["fields"].items():
        ftype = fdef["type"]

        if ftype in ["String", "Text", "Int", "Float", "Bool", "ID", "DateTime", "Date"] or ftype.startswith("List"):
            out["fields"][fname] = convert_primitive_field(fdef)

        elif ftype == "ManyToMany":
            base = fname[:-1] if fname.endswith("s") else fname
            new_name = f"{base}_ids"
            out["fields"][new_name] = {
                "type": FieldType.MANY_TO_MANY.value,
                "to": fdef["to"]
            }

        elif ftype == "OneToOne":
            out["fields"][fname] = {
                "type": FieldType.ONE_TO_ONE.value,
                "to": fdef["to"],
                "null": fdef.get("nullable", False),
                "blank": fdef.get("nullable", False),
            }

        elif ftype == "OneToMany":
            continue

        else:
            raise ValueError(f"Unknown type: {ftype}")

    # -------------------------------
    # 逆参照（OneToMany → ForeignKey）
    # -------------------------------
    for model_name, model_def in models.items():
        for fname, fdef in model_def["fields"].items():
            if fdef["type"] == "OneToMany" and fdef["to"] == target_model:

                nullable = fdef.get("nullable", False)

                # ★ 修正：親モデル名を FK 名にする
                field_name = model_name.lower()

                out["fields"][field_name] = {
                    "type": FieldType.FOREIGN_KEY.value,
                    "to": model_name,
                    "on_delete": "SET_NULL" if nullable else "CASCADE",
                }

                pk_name, pk_field = get_pk_field(models, model_name)
                if pk_field and "max_length" in pk_field:
                    out["fields"][field_name]["max_length"] = pk_field["max_length"]

                if nullable:
                    out["fields"][field_name]["null"] = True
                    out["fields"][field_name]["blank"] = True

    return out


# ---------------------------------------------------------
# run()（--spec 対応）
# ---------------------------------------------------------
def run(spec, output_file, input_files):
    cmp_paths = [Path(f).resolve() for f in input_files]

    spec_path = Path(spec)
    stem = spec_path.stem
    target_lower = stem.lower()

    models = load_owner_models(cmp_paths)
    yaml_keys = list(models.keys())

    target_model = None
    for key in yaml_keys:
        if key.lower() == target_lower:
            target_model = key
            break

    if target_model is None:
        print(f"[amcli] ERROR: Model '{stem}' not found in YAML keys: {yaml_keys}")
        raise RuntimeError(f"Model '{stem}' not found")

    result = build_reference_model(models, target_model)

    output_path = Path(output_file).resolve()

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated: {output_path}")
