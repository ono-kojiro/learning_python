#!/usr/bin/env python3

import sys
import getopt
import yaml
from jinja2 import Environment, FileSystemLoader


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> -l <loader.d> -d depend.yaml <model_yaml>...")


def read_yaml(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# Inline クラス生成
# ---------------------------------------------------------
def generate_inline_blocks(model_defs, children_map):
    inline_blocks = []

    for parent, child_list in children_map.items():
        for child in child_list:
            child_def = model_defs.get(child)
            if not child_def:
                continue

            fields = child_def.get("fields", {})
            inline_model_expr = None
            inline_class_name = None

            # 子モデルのフィールドを調べて親を参照しているものを探す
            for fname, fdef in fields.items():
                if fdef.get("to") != parent:
                    continue

                ftype = fdef.get("type")

                # ForeignKey / OneToOne → Inline
                if ftype in ("ForeignKey", "OneToOneField"):
                    inline_model_expr = f"{child}"
                    inline_class_name = f"{child}Inline"
                    break

                # ManyToMany → through モデルを Inline
                if ftype == "ManyToManyField":
                    inline_model_expr = f"{child}.{fname}.through"
                    inline_class_name = f"{child}{fname.capitalize()}Inline"
                    break

            if inline_model_expr:
                block = (
                    f"from myapp.models.{child.lower()}_model import {child}\n"
                    f"class {inline_class_name}(admin.TabularInline):\n"
                    f"    model = {inline_model_expr}\n"
                    f"    extra = 0\n"
                    f"    show_change_link = True\n\n"
                )
                inline_blocks.append(block)

    return inline_blocks


# ---------------------------------------------------------
# Admin クラス生成
# ---------------------------------------------------------
def generate_admin_blocks(model_defs, children_map):
    admin_blocks = []

    for model, data in model_defs.items():
        inline_classes = []

        # 子モデルの inline を収集
        for child in children_map.get(model, []):
            fields = model_defs[child].get("fields", {})
            for fname, fdef in fields.items():
                if fdef.get("to") != model:
                    continue

                ftype = fdef.get("type")

                if ftype in ("ForeignKey", "OneToOneField"):
                    inline_classes.append(f"{child}Inline")
                    break

                if ftype == "ManyToManyField":
                    inline_classes.append(f"{child}{fname.capitalize()}Inline")
                    break

        # Admin クラス本体
        if inline_classes:
            admin_body = f"    inlines = [{', '.join(inline_classes)}]"
        else:
            admin_body = "    pass"

        block = (
            f"class {model}Admin(admin.ModelAdmin):\n"
            f"{admin_body}\n\n"
            f"admin.site.register(models.{model}, {model}Admin)\n\n"
        )

        admin_blocks.append(block)

    return admin_blocks


# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:l:d:", ["help", "version", "output=", "loader=", "depend="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    loader_d = None
    depend_yaml = None

    for option, optarg in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-l", "--loader"):
            loader_d = optarg
        elif option in ("-d", "--depend"):
            depend_yaml = optarg

    if loader_d is None:
        print("ERROR: missing --loader", file=sys.stderr)
        sys.exit(1)

    if depend_yaml is None:
        print("ERROR: depend.yaml is required", file=sys.stderr)
        sys.exit(1)

    if not args:
        print("ERROR: model YAML files must be specified", file=sys.stderr)
        sys.exit(1)

    # depend.yaml 読み込み
    depend_map = read_yaml(depend_yaml)["dependencies"]

    # reverse dependency map
    children_map = {model: [] for model in depend_map}
    for model, deps in depend_map.items():
        for parent in deps:
            children_map[parent].append(model)

    # model YAML 読み込み
    model_defs = {}
    for filepath in args:
        data = read_yaml(filepath)
        model_defs[data["name"]] = data

    # Jinja2
    env = Environment(
        loader=FileSystemLoader(loader_d),
        autoescape=False
    )
    template = env.get_template("admin_template.j2")

    # 出力
    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    inline_blocks = generate_inline_blocks(model_defs, children_map)
    admin_blocks = generate_admin_blocks(model_defs, children_map)

    content = template.render(
        inline_blocks=inline_blocks,
        admin_blocks=admin_blocks,
    )

    fp.write(content)

    if output:
        fp.close()


if __name__ == "__main__":
    main()
