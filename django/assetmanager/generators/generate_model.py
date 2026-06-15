#!/usr/bin/env python3

import sys
import getopt
import yaml
from jinja2 import Environment, FileSystemLoader


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> -l <loader.d> -d depend.yaml <ref_yaml>...")


def read_yaml(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ------------------------------------------------------------
# フィールド行の生成
# ------------------------------------------------------------
def render_default(k, v):
    if k == "default" and (v in ["list", "dict"]):
        return f"default={v}"
    elif k == "on_delete":
        return f"{k}=models.{v}"
    else:
        return f"{k}={repr(v)}"


def render_simple_field(fname, field_def):
    args = []
    for k, v in field_def.items():
        if k == "type":
            continue
        if k is None:
            k = "null"
        args.append(render_default(k, v))
    arg_str = ", ".join(args)
    return f"{fname} = models.{field_def['type']}({arg_str})"


def render_relation_field(fname, field_def, ftype):
    args = []

    # to=
    args.append(f"to={repr(field_def['to'])}")

    # on_delete=
    val = field_def.get("on_delete", "CASCADE")
    if isinstance(val, str) and val.startswith("models."):
        args.append(f"on_delete={val}")
    else:
        args.append(f"on_delete=models.{val}")

    # その他
    for k, v in field_def.items():
        if k in ["type", "to", "on_delete"]:
            continue
        if k is None:
            k = "null"
        args.append(render_default(k, v))

    arg_str = ", ".join(args)
    return f"{fname} = models.{ftype}({arg_str})"


def render_many_to_many_field(fname, field_def, model_name):
    args = []

    # to='Device'
    args.append(repr(field_def["to"]))

    # その他
    for k, v in field_def.items():
        if k in ["type", "to"]:
            continue
        args.append(render_default(k, v))

    # related_name が無ければ自動付与
    if not any(a.startswith("related_name=") for a in args):
        args.append(f"related_name='{model_name.lower()}s'")

    arg_str = ", ".join(args)
    return f"{fname} = models.ManyToManyField({arg_str})"


# ------------------------------------------------------------
# __str__ の生成
# ------------------------------------------------------------
def generate_str_method(fields):
    id_field = None
    name_field = None
    address_field = None
    first_field = None

    for fname in fields:
        if first_field is None:
            first_field = fname
        if fname.endswith("_id"):
            id_field = fname
        if fname == "name":
            name_field = fname
        if fname == "address":
            address_field = fname

    if id_field:
        if name_field:
            return f'return f"{{self.{id_field}}}: {{self.{name_field}}}"'
        elif address_field:
            return f'return f"{{self.{id_field}}}: {{self.{address_field}}}"'
        else:
            return f'return f"{{self.{id_field}}}"'
    elif name_field:
        return f'return f"{{self.{name_field}}}"'
    elif address_field:
        return f'return f"{{self.{address_field}}}"'
    else:
        return f'return f"{{self.{first_field}}}"'


# ------------------------------------------------------------
# モデル 1 つ分の生成
# ------------------------------------------------------------
def generate_model_lines(data):
    name = data["name"]
    fields = data["fields"]

    field_lines = []

    for fname, field_def in fields.items():
        ftype = field_def["type"]

        # ForeignKey / OneToOne
        if ("ForeignKey" in ftype) or ("OneToOne" in ftype):
            model_ftype = "OneToOneField" if ftype == "OneToOne" else ftype
            line = render_relation_field(fname, field_def, model_ftype)
            field_lines.append(line)

        elif ftype == "ManyToManyField":
            line = render_many_to_many_field(fname, field_def, name)
            field_lines.append(line)

        else:
            line = render_simple_field(fname, field_def)
            field_lines.append(line)

    # __str__
    str_method = generate_str_method(list(fields.keys()))

    # Meta
    meta_lines = []
    if "meta" in data:
        for k, v in data["meta"].items():
            meta_lines.append(f"{k} = {repr(v)}")

    return field_lines, str_method, meta_lines


# ------------------------------------------------------------
# main
# ------------------------------------------------------------
def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:l:", ["help", "version", "output=", "loader="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    loader_d = None

    for option, optarg in options:
        if option in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-l", "--loader"):
            loader_d = optarg

    if loader_d is None:
        print("ERROR: missing --loader", file=sys.stderr)
        sys.exit(1)

    if not args:
        print("ERROR: no ref YAML files", file=sys.stderr)
        sys.exit(1)

    # Jinja2
    env = Environment(
        loader=FileSystemLoader(loader_d),
        autoescape=False
    )
    template = env.get_template("model_template.j2")

    # 出力
    if output:
        fp = open(output, mode="w", encoding="utf-8")
    else:
        fp = sys.stdout

    fp.write("# Generated by generate_model.py\n")
    fp.write("from django.db import models\n\n")

    # 各モデルを生成
    for filepath in args:
        data = read_yaml(filepath)
        model = data["name"]

        field_lines, str_method, meta_lines = generate_model_lines(data)

        content = template.render(
            model=model,
            field_lines=field_lines,
            str_method=str_method,
            meta_lines=meta_lines,
        )

        fp.write(content + "\n\n")

    if output:
        fp.close()


if __name__ == "__main__":
    main()
