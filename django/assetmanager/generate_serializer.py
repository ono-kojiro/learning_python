#!/usr/bin/env python3

import sys
import getopt
import yaml


def read_yaml_dict(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def main():
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

    deps = read_yaml_dict(depend_yml)
    dependencies = deps["dependencies"]
    reverse_dependencies = deps["reverse_dependencies"]

    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    fp.write("from rest_framework import serializers\n")
    fp.write("from myapp.models import *\n\n")

    for filepath in args:
        with open(filepath, mode="r", encoding="utf-8") as fp_in:
            data = yaml.safe_load(fp_in)

        model = data["name"]

        # import models only
        for dep in dependencies[model]:
            fp.write(f"from myapp.models import {dep}\n")
        fp.write(f"from myapp.models import {model}\n\n")

        fp.write(f"class {model}Serializer(serializers.ModelSerializer):\n")

        model_fields = ["id"]

        for fname, field_def in data["fields"].items():
            ftype = field_def["type"]

            # ForeignKey / OneToOneField
            if ftype in ("ForeignKey", "OneToOneField"):
                to_model = field_def["to"]
                null_allowed = field_def.get("null", False)
                blank_allowed = field_def.get("blank", False)

                fp.write(f"    {fname} = serializers.PrimaryKeyRelatedField(\n")
                fp.write(f"        queryset={to_model}.objects.all(),\n")

                required_flag = "False" if (null_allowed or blank_allowed) else "True"

                fp.write(f"        required={required_flag},\n")
                fp.write(f"        allow_null={'True' if null_allowed else 'False'},\n")
                fp.write("    )\n\n")

                model_fields.append(fname)

            # ManyToManyField
            elif ftype == "ManyToManyField":
                to_model = field_def["to"]

                fp.write(f"    {fname} = serializers.PrimaryKeyRelatedField(\n")
                fp.write("        many=True,\n")
                fp.write(f"        queryset={to_model}.objects.all(),\n")
                fp.write("        required=False,\n")
                fp.write("    )\n\n")

                model_fields.append(fname)

            # JSONField
            elif ftype == "JSONField":
                fp.write(f"    {fname} = serializers.ListField(\n")
                fp.write("        child=serializers.CharField(),\n")
                fp.write("        required=False,\n")
                fp.write("        default=list,\n")
                fp.write("    )\n\n")

                model_fields.append(fname)

            # CharField / その他
            else:
                is_id = field_def.get("id_field", False)

                if is_id:
                    fp.write(f"    {fname} = serializers.CharField(required=True)\n\n")
                else:
                    fp.write(f"    {fname} = serializers.CharField(required=False)\n\n")

                model_fields.append(fname)

        # reverse dependencies（read-only）
        for other_model in reverse_dependencies.get(model, []):
            reverse_field = f"{other_model.lower()}s"
            fp.write(
                f"    {reverse_field} = serializers.PrimaryKeyRelatedField(many=True, read_only=True)\n\n"
            )
            model_fields.append(reverse_field)

        # ★ DeviceSerializer の特別処理
        if model == "Device":
            # GET 用 managers
            fp.write(
                "    managers = serializers.PrimaryKeyRelatedField(\n"
                "        many=True,\n"
                "        read_only=True,\n"
                "        source='manager_set'\n"
                "    )\n\n"
            )
            model_fields.append("managers")

            # PATCH 用 managers
            fp.write(
                "    managers = serializers.PrimaryKeyRelatedField(\n"
                "        many=True,\n"
                "        queryset=Manager.objects.all(),\n"
                "        write_only=True,\n"
                "        required=False,\n"
                "    )\n\n"
            )

            # update() で置き換え
            fp.write(
                "    def update(self, instance, validated_data):\n"
                "        managers = validated_data.pop('managers', None)\n"
                "        instance = super().update(instance, validated_data)\n"
                "        if managers is not None:\n"
                "            instance.manager_set.set(managers)\n"
                "        return instance\n\n"
            )

        # Meta
        fp.write("    class Meta:\n")
        fp.write(f"        model = {model}\n")
        fp.write(f"        fields = {list(dict.fromkeys(model_fields))}\n\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
