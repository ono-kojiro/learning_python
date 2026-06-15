#!/usr/bin/env python3

import sys
import getopt
import yaml
from jinja2 import Environment, FileSystemLoader


def usage():
    print(
        f"Usage: {sys.argv[0]} "
        "-o <output> -l <loader_dir> -t <template.j2> --app-name <appname> schema.yaml"
    )
    sys.exit(1)


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def main():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "ho:l:t:",
            ["help", "output=", "loader=", "template=", "app-name="]
        )
    except getopt.GetoptError as e:
        print(str(e))
        usage()

    output = None
    loader_dir = None
    template_name = None
    app_name = None

    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-o", "--output"):
            output = val
        elif opt in ("-l", "--loader"):
            loader_dir = val
        elif opt in ("-t", "--template"):
            template_name = val
        elif opt == "--app-name":
            app_name = val

    if not output or not loader_dir or not template_name or not app_name:
        usage()

    if not args:
        print("ERROR: schema.yaml must be specified", file=sys.stderr)
        usage()

    schema_path = args[0]
    _schema = read_yaml(schema_path)  # 今は使わないが将来拡張のため読み込む

    # AppConfig クラス名
    app_class = app_name.capitalize() + "Config"

    # Jinja2 環境
    env = Environment(loader=FileSystemLoader(loader_dir), autoescape=False)
    template = env.get_template(template_name)

    # テンプレートレンダリング
    content = template.render(
        app_name=app_name,
        app_class=app_class,
    )

    # 出力
    with open(output, "w", encoding="utf-8") as fp:
        fp.write(content + "\n")


if __name__ == "__main__":
    main()
