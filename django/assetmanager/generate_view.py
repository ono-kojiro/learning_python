#!/usr/bin/env python3

import sys
import getopt
import yaml


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")


def load_categories():
    with open("category.yaml", "r", encoding="utf-8") as fp:
        data = yaml.safe_load(fp)
    return data.get("categories", {})


def find_natural_key(fields):
    """
    *_id かつ CharField かつ unique=True を自然キーとみなす
    """
    for fname, fdef in fields.items():
        if fname.endswith("_id"):
            if fdef.get("type") == "CharField" and fdef.get("unique", False):
                return fname
    return None


def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:", ["help", "version", "output="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    for option, optarg in options:
        if option in ("-o", "--output"):
            output = optarg

    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    categories = load_categories()

    for filepath in args:
        with open(filepath, mode="r", encoding="utf-8") as fp_in:
            data = yaml.safe_load(fp_in)

        model = data["name"]
        model_lower = model.lower()
        serializer = f"{model}Serializer"
        fields = data["fields"]

        fp.write("from django.apps import apps\n")
        fp.write("from rest_framework import viewsets\n\n")

        fp.write(f"class {model}ViewSet(viewsets.ModelViewSet):\n")
        fp.write("    queryset = None\n\n")

        fp.write("    def get_queryset(self):\n")
        fp.write(f"        Model = apps.get_model('myapp', '{model}')\n")
        fp.write("        return Model.objects.all()\n\n")

        fp.write("    def get_serializer_class(self):\n")
        fp.write(f"        from myapp.serializers.{model_lower}_serializer import {serializer}\n")
        fp.write(f"        return {serializer}\n\n")

        # ★ lookup_field の決定ロジック
        category = categories.get(model, "resource")

        if model == "Comment":
            # Comment は comment_id を使う（テスト仕様）
            fp.write('    lookup_field = "id"\n\n')

        elif category == "attribute":
            # attribute は自然キーがあっても id を使う
            fp.write('    lookup_field = "id"\n\n')

        elif category == "owner":
            # owner は常に id
            fp.write('    lookup_field = "id"\n\n')

        else:
            # resource → 自然キーを探す
            natural_key = find_natural_key(fields)
            if natural_key:
                fp.write(f'    lookup_field = "{natural_key}"\n\n')
            else:
                fp.write('    lookup_field = "id"\n\n')

    if output:
        fp.close()


if __name__ == "__main__":
    main()
