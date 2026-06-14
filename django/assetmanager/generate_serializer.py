#!/usr/bin/env python3

import sys
import getopt
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def usage():
    print(f"Usage: {sys.argv[0]} -o <output> -l <loader.d> -d depend.yaml -c category.yaml <model_yaml>...")


def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:l:d:c:",
            [
                "help",
                "version",
                "output=",
                "loader=",
                "depend=",
                "category=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    loader_d = None
    depend_yml = None
    category_yml = None

    for option, optarg in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-l", "--loader"):
            loader_d = optarg
        elif option in ("-d", "--depend"):
            depend_yml = optarg
        elif option in ("-c", "--category"):
            category_yml = optarg

    # 必須チェック
    if loader_d is None:
        print("ERROR: missing --loader", file=sys.stderr)
        sys.exit(1)
    if depend_yml is None or category_yml is None:
        print("ERROR: missing -d or -c", file=sys.stderr)
        sys.exit(1)

    # 依存関係とカテゴリを読み込み
    deps = read_yaml(depend_yml)
    dependencies = deps["dependencies"]
    reverse_dependencies = deps["reverse_dependencies"]

    categories = read_yaml(category_yml)
    general_categories = categories["general_categories"]
    dependency_categories = categories["dependency_categories"]

    # Jinja2 環境
    env = Environment(
        loader=FileSystemLoader(loader_d),
        autoescape=False
    )

    # 出力先
    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    # モデルごとに生成
    for filepath in args:
        data = read_yaml(filepath)
        model = data["name"]
        fields = data["fields"]

        # カテゴリ判定
        dep_cat = dependency_categories.get(model)

        # テンプレート自動選択
        if dep_cat == "m2m_owner":
            template_name = "serializer_m2m_owner.j2"
        elif dep_cat == "m2m_target":
            template_name = "serializer_m2m_target.j2"
        elif dep_cat == "fk_parent":
            template_name = "serializer_fk_parent.j2"
        else:
            template_name = "serializer_normal.j2"

        template = env.get_template(template_name)

        # fields_list は Meta.fields 用
        fields_list = ["id"] + list(fields.keys())

        content = template.render(
            model=model,
            fields=fields,
            fields_list=fields_list,
            reverse_dependencies=reverse_dependencies,
        )

        fp.write(content + "\n\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
