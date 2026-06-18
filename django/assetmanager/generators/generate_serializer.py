#!/usr/bin/env python3

import sys
import getopt
import yaml
from jinja2 import Environment, FileSystemLoader


def usage():
    print(f"Usage: {sys.argv[0]} -o <output> -l <loader.d> -s schema.yaml <model_yaml>...")


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


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
                "schema=",
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

    # 必須チェック
    if loader_d is None:
        print("ERROR: missing --loader", file=sys.stderr)
        sys.exit(1)
    if schema_yaml is None:
        print("ERROR: missing --schema", file=sys.stderr)
        sys.exit(1)

    # schema.yaml を読み込む
    schema = read_yaml(schema_yaml)
    dependencies = schema["dependencies"]
    reverse_dependencies = schema["reverse_dependencies"]
    dependency_categories = schema["dependency_categories"]
    nested_map = schema.get("nested", {})   # ★ nested セクション

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

        # fields_list の構築（Meta.fields 用）
        fields_list = ["id"] + list(fields.keys())

        # reverse FK を追加（fk_parent の場合のみ）
        rev = reverse_dependencies.get(model, [])
        for other_model in rev:
            fields_list.append(f"{other_model.lower()}s")

        # ★ nested 構造を schema.yaml から取得
        nested_fields = nested_map.get(model, [])

        # テンプレートへ渡す
        content = template.render(
            model=model,
            fields=fields,
            fields_list=fields_list,
            reverse_dependencies=reverse_dependencies,
            nested_fields=nested_fields,   # ★ 追加
        )

        fp.write(content + "\n\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
