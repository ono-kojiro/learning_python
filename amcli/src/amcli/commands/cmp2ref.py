from pathlib import Path
import yaml
import json


def load_owner_models(paths):
    models = {}
    for path in paths:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            models.update(data)
    return models


def convert_primitive_field(fdef):
    out = {}
    ftype = fdef["type"]

    if ftype == "String":
        out["type"] = "CharField"
        out["max_length"] = fdef.get("max_length", 255)

    elif ftype == "Text":
        out["type"] = "TextField"

    elif ftype == "Int":
        out["type"] = "IntegerField"

    elif ftype == "Float":
        out["type"] = "FloatField"

    elif ftype == "Bool":
        out["type"] = "BooleanField"

    elif ftype == "ID":
        out["type"] = "CharField"
        out["max_length"] = fdef.get("max_length", 100)
        out["unique"] = True

    elif ftype.startswith("List"):
        out["type"] = "JSONField"

    else:
        raise ValueError(f"Unknown primitive type: {ftype}")

    if "unique" in fdef:
        out["unique"] = fdef["unique"]

    if "default" in fdef:
        out["default"] = fdef["default"]

    if "help" in fdef:
        out["help_text"] = fdef["help"]

    return out


def get_pk_field(models, model_name):
    fields = models[model_name]["fields"]
    for fname, fdef in fields.items():
        if fdef.get("unique") and fdef["type"] in ["String", "ID"]:
            return fname, convert_primitive_field(fdef)
    return None, None


def build_reference_model(models, target_model):
    if target_model not in models:
        raise ValueError(f"Model {target_model} not found")

    out = {
        "name": target_model,
        "meta": models[target_model].get("meta", {}),
        "fields": {}
    }

    for fname, fdef in models[target_model]["fields"].items():
        ftype = fdef["type"]

        if ftype in ["String", "Text", "Int", "Float", "Bool", "ID"] or ftype.startswith("List"):
            out["fields"][fname] = convert_primitive_field(fdef)

        elif ftype == "ManyToMany":
            base = fname[:-1] if fname.endswith("s") else fname
            new_name = f"{base}_ids"
            out["fields"][new_name] = {
                "type": "ManyToManyField",
                "to": fdef["to"]
            }

        elif ftype == "OneToOne":
            out["fields"][fname] = {
                "type": "OneToOneField",
                "to": fdef["to"],
                "null": fdef.get("nullable", False),
                "blank": fdef.get("nullable", False),
            }

        elif ftype == "OneToMany":
            continue

        else:
            raise ValueError(f"Unknown type: {ftype}")

    for model_name, model_def in models.items():
        for fname, fdef in model_def["fields"].items():
            ftype = fdef["type"]

            pk_name, pk_field = get_pk_field(models, model_name)

            if ftype == "OneToMany" and fdef["to"] == target_model:
                nullable = fdef.get("nullable", False)
                field_name = f"{model_name.lower()}_id"

                out["fields"][field_name] = {
                    "type": "ForeignKey",
                    "to": model_name,
                    "on_delete": "SET_NULL" if nullable else "CASCADE",
                }

                if pk_field and "max_length" in pk_field:
                    out["fields"][field_name]["max_length"] = pk_field["max_length"]

                if nullable:
                    out["fields"][field_name]["null"] = True
                    out["fields"][field_name]["blank"] = True

    return out


def run(entity_name, output_file, input_files):
    cmp_paths = [Path(f).resolve() for f in input_files]

    target = None
    for p in cmp_paths:
        if p.name.lower() == f"{entity_name.lower()}.yml":
            target = p
            break

    if target is None:
        print(f"[amcli] ERROR: {entity_name}.yml not found in input files")
        return

    model_name = target.stem
    model_name = model_name[0].upper() + model_name[1:]

    models = load_owner_models(cmp_paths)

    result = build_reference_model(models, model_name)

    output_path = Path(output_file).resolve()

    # JSON で出力
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated: {output_path}")
