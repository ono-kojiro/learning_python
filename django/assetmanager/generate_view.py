#!/usr/bin/env python3

import sys
import getopt
import yaml


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")


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
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg

    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    for filepath in args:
        with open(filepath, mode="r", encoding="utf-8") as fp_in:
            data = yaml.safe_load(fp_in)

        model = data["name"]
        model_lower = model.lower()
        serializer = f"{model}Serializer"

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

        # ★ lookup_field の特別ルール
        if model == "Device":
            fp.write('    lookup_field = "device_id"\n\n')
        elif model == "Manager":
            fp.write('    lookup_field = "id"\n\n')
        else:
            # *_id を探す
            id_field = None
            for fname in data["fields"].keys():
                if fname.endswith("_id"):
                    id_field = fname
                    break

            if id_field:
                fp.write(f'    lookup_field = "{id_field}"\n\n')
            else:
                fp.write('    lookup_field = "id"\n\n')

    if output:
        fp.close()


if __name__ == "__main__":
    main()
