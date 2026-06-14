#!/usr/bin/env python3

import sys
import getopt
import yaml
from jinja2 import Environment, FileSystemLoader


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> -l <loader.d> -t <template.j2> <input>...")


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:l:t:",
            [
                "help",
                "version",
                "output=",
                "loader=",
                "template=",
            ]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    loader_d = None
    template_j2 = None

    for option, optarg in options:
        if option in ("-o", "--output"):
            output = optarg
        if option in ("-l", "--loader"):
            loader_d = optarg
        if option in ("-t", "--template"):
            template_j2 = optarg

    if loader_d is None:
        print("ERROR: no loader option", file=sys.stderr)
        ret += 1

    if template_j2 is None:
        print("ERROR: no template option", file=sys.stderr)
        ret += 1

    if ret:
        sys.exit(ret)

    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    # Jinja2 環境
    env = Environment(
        loader=FileSystemLoader(loader_d),
        autoescape=False
    )
    template = env.get_template(template_j2)

    if not args:
        print("ERROR: no input YAML files", file=sys.stderr)
        usage()
        sys.exit(1)

    # モデル名を収集
    models = []
    for filepath in args:
        data = read_yaml(filepath)
        models.append(data["name"])

    # テンプレートレンダリング
    content = template.render(
        models=models,
    )

    fp.write(content + "\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
