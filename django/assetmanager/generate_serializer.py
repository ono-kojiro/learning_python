#!/usr/bin/env python3

import sys
import getopt
import yaml


def read_yaml_dict(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def main():
    # ---------------------------------------------------------
    # Parse options
    # ---------------------------------------------------------
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:d:", ["help", "version", "output=", "depend="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    depend_yml = None

    for option, optarg in options:
        if option in ("-h", "--help"):
            print(f"Usage: {sys.argv[0]} -o <output> -d depend.yaml <model_yaml>...")
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-d", "--depend"):
            depend_yml = optarg

    if depend_yml is None:
        print("ERROR: no depend option", file=sys.stderr)
        sys.exit(1)

    if not args:
        print("ERROR: no model YAML files", file=sys.stderr)
        sys.exit(1)

    # ---------------------------------------------------------
    # Load depend.yaml
    # ---------------------------------------------------------
    deps = read_yaml_dict(depend_yml)
    dependencies = deps["dependencies"]
    reverse_dependencies = deps["reverse_dependencies"]

    # ---------------------------------------------------------
    # Output file
    # ---------------------------------------------------------
    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    fp.write("from rest_framework import serializers\n")

    # ---------------------------------------------------------
    # Generate serializers
    # ---------------------------------------------------------
    for filepath in args:
        with open(filepath, mode="r", encoding="utf-8") as fp_in:
            data = yaml.safe_load(fp_in)

        model = data["name"]

        # import models
        for dep in dependencies[model]:
            fp.write(f"from myapp.models import {dep}\n")
        fp.write(f"from myapp.models import {model}\n\n")

        # import dependent serializers
        for dep in dependencies[model]:
            fp.write(f"from myapp.serializers import {dep}Serializer\n")
        fp.write("\n")

        # Serializer class
        fp.write(f"class {model}Serializer(serializers.ModelSerializer):\n")

        model_fields = ["id"]

        # ---------------------------------------------------------
        # 自分のフィールド
        # ---------------------------------------------------------
        for fname, field_def in data["fields"].items():
            ftype = field_def["type"]

            # ForeignKey / OneToOne
            if ftype in ("ForeignKey", "OneToOneField"):
                to_model = field_def["to"]

                fp.write(f"    # for read\n")
                fp.write(f"    {fname} = {to_model}Serializer(read_only=True)\n\n")

                fp.write(f"    # for write\n")
                fp.write(f"    {fname}_id = serializers.PrimaryKeyRelatedField(\n")
                fp.write(f"        queryset={to_model}.objects.all(),\n")
                fp.write(f"        write_only=True,\n")
                fp.write(f"        source=\"{fname}\",\n")

                null_allowed = field_def.get("null", False)
                blank_allowed = field_def.get("blank", False)

                fp.write(f"        allow_null={'True' if null_allowed else 'False'},\n")
                fp.write(f"        required={'False' if (null_allowed or blank_allowed) else 'True'},\n")
                fp.write("    )\n\n")

                model_fields.append(fname)
                model_fields.append(f"{fname}_id")

            # ManyToMany
            elif ftype == "ManyToManyField":
                to_model = field_def["to"]

                fp.write(f"    {fname} = serializers.PrimaryKeyRelatedField(\n")
                fp.write("        many=True,\n")
                fp.write(f"        queryset={to_model}.objects.all(),\n")
                fp.write("    )\n\n")

                model_fields.append(fname)

            # 普通のフィールド
            else:
                model_fields.append(fname)

        # ---------------------------------------------------------
        # 逆向き依存フィールド（Meta の前に必ず出力）
        # ---------------------------------------------------------
        for other_model in reverse_dependencies.get(model, []):
            # 他モデルの YAML を探す
            for other_filepath in args:
                with open(other_filepath, mode="r", encoding="utf-8") as fp_other:
                    other_data = yaml.safe_load(fp_other)

                if other_data["name"] != other_model:
                    continue

                for ofname, ofdef in other_data["fields"].items():
                    if ofdef.get("to") != model:
                        continue

                    # ManyToMany の逆側
                    if ofdef["type"] == "ManyToManyField":
                        reverse_field = f"{other_model.lower()}s"
                        fp.write(f"    {reverse_field} = serializers.PrimaryKeyRelatedField(many=True, read_only=True)\n\n")
                        model_fields.append(reverse_field)

                    # ForeignKey / OneToOne の逆側
                    elif ofdef["type"] in ("ForeignKey", "OneToOneField"):
                        reverse_field = f"{other_model.lower()}s"
                        fp.write(f"    {reverse_field} = serializers.PrimaryKeyRelatedField(many=True, read_only=True)\n\n")
                        model_fields.append(reverse_field)

        # ---------------------------------------------------------
        # Meta クラス（最後）
        # ---------------------------------------------------------
        fp.write("    class Meta:\n")
        fp.write(f"        model = {model}\n")

        all_fields = list(dict.fromkeys(model_fields))
        fp.write(f"        fields = {all_fields}\n\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
