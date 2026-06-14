#!/usr/bin/env python3

import yaml
import sys
import getopt


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

        # プリミティブ型
        if ftype in ["String", "Text", "Int", "Float", "Bool", "ID"] or ftype.startswith("List"):
            out["fields"][fname] = convert_primitive_field(fdef)

        # ManyToMany
        elif ftype == "ManyToMany":
            base = fname[:-1] if fname.endswith("s") else fname
            new_name = f"{base}_ids"
            out["fields"][new_name] = {
                "type": "ManyToManyField",
                "to": fdef["to"]
            }

        # ★ OneToOne → OneToOneField として生成
        elif ftype == "OneToOne":
            out["fields"][fname] = {
                "type": "OneToOneField",
                "to": fdef["to"],
                "null": fdef.get("nullable", False),
                "blank": fdef.get("nullable", False),
            }

        # OneToMany はスキップ（逆参照で処理）
        elif ftype == "OneToMany":
            continue

        else:
            raise ValueError(f"Unknown type: {ftype}")

    # 逆参照（OneToMany のみ）
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


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "",
            ["name=", "output="]
        )
    except getopt.GetoptError as e:
        print(str(e))
        print("Usage: python cmp2ref.py --name <ModelName> [--output file] <yaml1> <yaml2> ...")
        sys.exit(1)

    target_model = None
    output_file = None

    for opt, val in opts:
        if opt == "--name":
            target_model = val
        elif opt == "--output":
            output_file = val

    if not target_model:
        print("Error: --name <ModelName> is required")
        sys.exit(1)

    if len(args) == 0:
        print("Error: YAML files must be specified")
        sys.exit(1)

    models = load_owner_models(args)
    result = build_reference_model(models, target_model)

    yaml_text = yaml.dump(result, sort_keys=False)

    if output_file:
        with open(output_file, "w") as f:
            f.write('---\n')
            f.write('# {0}\n'.format(output_file))
            f.write(yaml_text)
        print(f"Generated: {output_file}")
    else:
        print(yaml_text)


if __name__ == "__main__":
    main()
