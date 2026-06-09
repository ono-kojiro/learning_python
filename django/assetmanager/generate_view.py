#!/usr/bin/env python3

import sys
import getopt
import yaml


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")


def main():
    ret = 0

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

        # Router が basename を自動決定できるようにする
        fp.write("    queryset = None\n\n")

        # get_queryset
        fp.write("    def get_queryset(self):\n")
        fp.write(f"        Model = apps.get_model('myapp', '{model}')\n")
        fp.write("        return Model.objects.all()\n\n")

        # get_serializer_class
        fp.write("    def get_serializer_class(self):\n")
        fp.write(f"        from myapp.serializers.{model_lower}_serializer import {serializer}\n")
        fp.write(f"        return {serializer}\n\n")

        # lookup_field
        lookup_field = None
        for fname in data["fields"].keys():
            if fname.endswith("_id") and fname != "id":
                lookup_field = fname
                break

        if lookup_field:
            fp.write(f'    lookup_field = "{lookup_field}"\n')

        fp.write("\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
