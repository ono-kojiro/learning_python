#!/usr/bin/env python3

import sys
import re

import getopt
import yaml

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:d:",
            [
                "help",
                "version",
                "output=",
                "depend=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    depend_yaml = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-d", "--depend"):
            depend_yaml = optarg
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if depend_yaml is None:
        print('ERROR: no depend option', file=sys.stderr)
        ret += 1

    if ret != 0:
        sys.exit(ret)

    depend_map = read_yaml(depend_yaml)["dependencies"]

    # 逆依存関係（親 → 子）を構築
    children = {model: [] for model in depend_map}
    for model, deps in depend_map.items():
        for parent in deps:
            children[parent].append(model)

    fp.write('from django.contrib import admin\n')
    fp.write("from myapp import models\n")

    for filepath in args:
        fp_in = open(filepath, mode="r", encoding="utf-8")
        data = yaml.safe_load(fp_in)

        model = data['name']

        # このモデルの子モデルを取得
        child_models = children.get(model, [])

        fp.write('from myapp.models import {0}\n'.format(model))
        fp.write('\n')

        # Inline クラスを生成
        for child in child_models:
            fp.write(f"class {child}Inline(admin.TabularInline):\n")
            fp.write(f"    model = models.{child}\n")
            fp.write("    extra = 0\n")
            fp.write("    show_change_link = True\n\n")

        # Admin クラスを生成
        fp.write(f"@admin.register(models.{model})\n")
        fp.write(f"class {model}Admin(admin.ModelAdmin):\n")

        if child_models:
            inline_list = ", ".join([f"{child}Inline" for child in child_models])
            fp.write(f"    inlines = [{inline_list}]\n")
        else:
            fp.write("    pass\n")

        #fp.write('admin.site.register({0})\n'.format(model))
        
        fp_in.close()

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

