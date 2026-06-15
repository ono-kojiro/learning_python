#!/usr/bin/env python3

import sys
import getopt
import yaml
from jinja2 import Environment, FileSystemLoader


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> -l <loader.d> --meta meta.yaml <model_ref_yaml>")


def read_yaml(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# Inline クラス生成（対象モデルの子モデルのみ）
# ---------------------------------------------------------
def generate_inline_blocks(target_model, model_defs, children_map):
    inline_blocks = []
    inline_class_names = []

    for child in children_map.get(target_model, []):
        child_def = model_defs.get(child)
        if not child_def:
            continue

        fields = child_def.get("fields", {})
        inline_model_expr = None
        inline_class_name = None

        # 子モデルのフィールドを調べて親を参照しているものを探す
        for fname, fdef in fields.items():
            if fdef.get("to") != target_model:
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
            inline_class_names.append(inline_class_name)

    return inline_blocks, inline_class_names


# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:l:s:",
            [
                "help",
                "version",
                "output=",
                "loader=",
                "schema="
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    loader_d = None
    schema_yaml = None

    for option, optarg in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-l", "--loader"):
            loader_d = optarg
        elif option in ("-s", "--schema"):
            schema_yaml = optarg

    if loader_d is None:
        print("ERROR: missing --loader", file=sys.stderr)
        sys.exit(1)

    if schema_yaml is None:
        print("ERROR: missing --schema", file=sys.stderr)
        sys.exit(1)

    if not args:
        print("ERROR: model_ref YAML must be specified", file=sys.stderr)
        sys.exit(1)

    # 対象モデルを ref_yaml から取得
    ref_yaml = args[0]
    ref_data = read_yaml(ref_yaml)
    target_model = ref_data["name"]

    # meta.yaml 読み込み
    schema = read_yaml(schema_yaml)
    depend_map = schema["dependencies"]
    model_defs = schema["models"]

    # reverse dependency map
    children_map = {model: [] for model in depend_map}
    for model, deps in depend_map.items():
        for parent in deps:
            children_map[parent].append(model)

    # Jinja2
    env = Environment(
        loader=FileSystemLoader(loader_d),
        autoescape=False
    )
    template = env.get_template("admin_template.j2")

    # Inline と Admin クラス生成
    inline_blocks, inline_class_names = generate_inline_blocks(
        target_model, model_defs, children_map
    )

    content = template.render(
        model=target_model,
        inline_blocks=inline_blocks,
        inline_class_names=inline_class_names,
    )

    # 出力
    if output:
        with open(output, "w", encoding="utf-8") as fp:
            fp.write(content)
    else:
        print(content)


if __name__ == "__main__":
    main()
