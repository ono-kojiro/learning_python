#!/usr/bin/env python3

import sys
import getopt
import yaml


def read_yaml_dict(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ============================================================
# m2m_owner（Manager）
# ============================================================
def generate_serializer_m2m_owner(fp, model, fields):
    fp.write(
        "    device_ids = serializers.PrimaryKeyRelatedField(\n"
        "        many=True,\n"
        "        queryset=Device.objects.all(),\n"
        "        required=False,\n"
        "    )\n\n"
    )

    fp.write(
        "    devices = serializers.PrimaryKeyRelatedField(\n"
        "        many=True,\n"
        "        queryset=Device.objects.all(),\n"
        "        source='device_ids',\n"
        "        required=False,\n"
        "    )\n\n"
    )

    fp.write(
        "    def update(self, instance, validated_data):\n"
        "        device_ids = validated_data.pop('device_ids', None)\n"
        "        instance = super().update(instance, validated_data)\n"
        "        if device_ids is not None:\n"
        "            instance.device_ids.set(device_ids)\n"
        "        return instance\n\n"
    )

    fp.write("    class Meta:\n")
    fp.write(f"        model = {model}\n")
    fp.write(
        "        fields = [\n"
        "            'id',\n"
        "            'manager_id',\n"
        "            'name',\n"
        "            'email',\n"
        "            'device_ids',\n"
        "            'devices',\n"
        "        ]\n\n"
    )


# ============================================================
# m2m_target（Device）
# ============================================================
def generate_serializer_m2m_target(fp, model, fields):
    fp.write(
        "    managers = serializers.PrimaryKeyRelatedField(\n"
        "        many=True,\n"
        "        queryset=Manager.objects.all(),\n"
        "        required=False,\n"
        "    )\n\n"
    )

    fp.write(
        "    netifs = serializers.PrimaryKeyRelatedField(\n"
        "        many=True,\n"
        "        read_only=True,\n"
        "        source='netif_set'\n"
        "    )\n\n"
    )

    fp.write(
        "    def update(self, instance, validated_data):\n"
        "        managers = validated_data.pop('managers', None)\n"
        "        instance = super().update(instance, validated_data)\n"
        "        if managers is not None:\n"
        "            instance.managers.set(managers)\n"
        "        return instance\n\n"
    )

    fp.write(
        "    def to_representation(self, instance):\n"
        "        rep = super().to_representation(instance)\n"
        "        if 'managers' in rep:\n"
        "            rep['managers'] = sorted(rep['managers'])\n"
        "        return rep\n\n"
    )

    fp.write("    class Meta:\n")
    fp.write(f"        model = {model}\n")
    fp.write(
        "        fields = [\n"
        "            'id',\n"
        "            'device_id',\n"
        "            'name',\n"
        "            'serial_number',\n"
        "            'managers',\n"
        "            'netifs',\n"
        "        ]\n\n"
    )


# ============================================================
# fk_parent（NetIF）
# ============================================================
def generate_serializer_fk_parent(fp, model, fields, reverse_dependencies):
    model_fields = ["id"]

    for fname, field_def in fields.items():
        ftype = field_def["type"]

        if ftype == "ForeignKey":
            to_model = field_def["to"]
            fp.write(
                f"    {fname} = serializers.PrimaryKeyRelatedField(queryset={to_model}.objects.all())\n\n"
            )
        else:
            fp.write(f"    {fname} = serializers.CharField(required=False)\n\n")

        model_fields.append(fname)

    # reverse FK
    for other_model in reverse_dependencies.get(model, []):
        reverse_field = f"{other_model.lower()}s"
        fp.write(
            f"    {reverse_field} = serializers.PrimaryKeyRelatedField(many=True, read_only=True)\n\n"
        )
        model_fields.append(reverse_field)

    fp.write("    class Meta:\n")
    fp.write(f"        model = {model}\n")
    fp.write(f"        fields = {model_fields}\n\n")


# ============================================================
# 通常モデル（fk_child / no_dependency）
# ============================================================
def generate_serializer_normal(fp, model, fields):
    model_fields = ["id"]

    for fname, field_def in fields.items():
        ftype = field_def["type"]

        if ftype == "ForeignKey":
            to_model = field_def["to"]
            fp.write(
                f"    {fname} = serializers.PrimaryKeyRelatedField(queryset={to_model}.objects.all())\n\n"
            )
        else:
            fp.write(f"    {fname} = serializers.CharField(required=False)\n\n")

        model_fields.append(fname)

    fp.write("    class Meta:\n")
    fp.write(f"        model = {model}\n")
    fp.write(f"        fields = {model_fields}\n\n")


# ============================================================
# generate_serializer（ディスパッチャ）
# ============================================================
def generate_serializer(fp, data, dependencies, reverse_dependencies,
                        general_category, dependency_category):

    model = data["name"]
    fields = data["fields"]

    fp.write(f"# Generated by generate_serializer.py for {model}\n")
    fp.write("from rest_framework import serializers\n")
    fp.write("from myapp.models import *\n\n")

    fp.write(f"class {model}Serializer(serializers.ModelSerializer):\n")

    # カテゴリ別ディスパッチ
    if dependency_category == "m2m_owner":
        return generate_serializer_m2m_owner(fp, model, fields)

    if dependency_category == "m2m_target":
        return generate_serializer_m2m_target(fp, model, fields)

    if dependency_category == "fk_parent":
        return generate_serializer_fk_parent(fp, model, fields, reverse_dependencies)

    # fk_child / no_dependency
    return generate_serializer_normal(fp, model, fields)


# ============================================================
# main
# ============================================================
def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:d:c:", ["help", "version", "output=", "depend=", "category="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    depend_yml = None
    category_yml = None

    for option, optarg in options:
        if option in ("-h", "--help"):
            print(f"Usage: {sys.argv[0]} -o <output> -d depend.yaml -c category.yaml <model_yaml>...")
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-d", "--depend"):
            depend_yml = optarg
        elif option in ("-c", "--category"):
            category_yml = optarg

    if depend_yml is None or category_yml is None:
        print("ERROR: missing -d or -c", file=sys.stderr)
        sys.exit(1)

    deps = read_yaml_dict(depend_yml)
    dependencies = deps["dependencies"]
    reverse_dependencies = deps["reverse_dependencies"]

    categories = read_yaml_dict(category_yml)
    general_categories = categories["general_categories"]
    dependency_categories = categories["dependency_categories"]

    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    for filepath in args:
        with open(filepath, mode="r", encoding="utf-8") as fp_in:
            data = yaml.safe_load(fp_in)

        model = data["name"]
        generate_serializer(
            fp,
            data,
            dependencies,
            reverse_dependencies,
            general_categories.get(model),
            dependency_categories.get(model),
        )

    if output:
        fp.close()


if __name__ == "__main__":
    main()
