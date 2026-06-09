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
            sys.argv[1:],
            "hvo:",
            [
                "help",
                "version",
                "output=",
            ],
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
        fp = open(output, mode="w", encoding="utf-8")
    else:
        fp = sys.stdout

    fp.write("from rest_framework import routers\n")

    models = []

    # Load model names
    for filepath in args:
        with open(filepath, mode="r", encoding="utf-8") as fp_in:
            data = yaml.safe_load(fp_in)
            models.append(data["name"])

    # Import ViewSets
    for model in models:
        fp.write(f"from myapp.views.{model.lower()}_view import {model}ViewSet\n")

    fp.write("\n")
    fp.write("router = routers.DefaultRouter()\n\n")

    # Register with basename
    for model in models:
        basename = model.lower()
        fp.write(
            f'router.register(r"{basename}s", {model}ViewSet, basename="{basename}")\n'
        )

    fp.write("\nurlpatterns = router.urls\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
