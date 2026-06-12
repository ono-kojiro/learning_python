#!/usr/bin/env python3

import sys
import re
import getopt
import yaml
from pprint import pprint


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")


def read_yaml(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def render_default(k, v):
    if k == "default" and (v in ["list", "dict"]):
        return f"default={v}"
    elif k == "on_delete":
        return f"{k}=models.{v}"
    else:
        return f"{k}={repr(v)}"


def render_simple_field(field_def):
    args = []
    for k, v in field_def.items():
        if k == "type":
            continue
        if k is None:
            k = "null"
        args.append(render_default(k, v))
    return args


def render_relation_field(field_def, ftype):
    args = []

    # to=
    args.append(f"to={repr(field_def['to'])}")

    # on_delete=
    val = field_def.get("on_delete", "CASCADE")
    if val.startswith("models."):
        args.append(f"on_delete={val}")
    else:
        args.append(f"on_delete=models.{val}")

    # その他の属性
    for k, v in field_def.items():
        if k in ["type", "to", "on_delete"]:
            continue
        if k is None:
            k = "null"
        args.append(render_default(k, v))

    return args


def generate_model(fp, data):
    name = data["name"]

    fp.write(f"class {name}(models.Model):\n")

    # YAML の fields をそのままモデル化
    for fname, field_def in data["fields"].items():
        ftype = field_def["type"]

        if ftype in ["ForeignKey", "OneToOneField"]:
            args = render_relation_field(field_def, ftype)
        else:
            args = render_simple_field(field_def)

        arg_str = ", ".join(args)
        fp.write(f"    {fname} = models.{ftype}({arg_str})\n")

    # IPv4 の address フィールドは特別扱い
    if name == "IPv4" and "address" not in data["fields"]:
        fp.write(
            "    address = models.CharField(max_length=255, null=True, blank=True)\n"
        )

    # __str__ の生成
    fp.write("\n")
    fp.write("    def __str__(self):\n")

    # IPv4 の特別処理
    if name == "IPv4":
        fp.write("        if self.addresses and len(self.addresses) > 0:\n")
        fp.write('            return f"{self.ipv4_id}: {self.addresses[0]}"\n')
        fp.write('        return f"{self.ipv4_id} (no IP address)"\n')
        return

    id_field = None
    name_field = None
    address_field = None
    first_field = None

    all_fields = list(data["fields"].keys())
    if name == "IPv4" and "address" not in all_fields:
        all_fields.append("address")

    for fname in all_fields:
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
            fp.write(f'        return f"{{self.{id_field}}}: {{self.{name_field}}}"\n')
        elif address_field:
            fp.write(f'        return f"{{self.{id_field}}}: {{self.{address_field}}}"\n')
        else:
            fp.write(f'        return f"{{self.{id_field}}}"\n')
    elif name_field:
        fp.write(f'        return f"{{self.{name_field}}}"\n')
    elif address_field:
        fp.write(f'        return f"{{self.{address_field}}}"\n')
    else:
        fp.write(f'        return f"{{self.{first_field}}}"\n')

    # Meta
    if "meta" in data:
        fp.write("\n")
        fp.write("    class Meta:\n")
        for k, v in data["meta"].items():
            fp.write(f"        {k} = {repr(v)}\n")


def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:d:", ["help", "version", "output=", "depend="]
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

    if depend_yaml is None:
        print("ERROR: no depend option", file=sys.stderr)
        sys.exit(1)

    depend_map = read_yaml(depend_yaml)["dependencies"]

    if output:
        fp = open(output, mode="w", encoding="utf-8")
    else:
        fp = sys.stdout

    fp.write("from django.db import models\n\n")

    for filepath in args:
        data = read_yaml(filepath)
        generate_model(fp, data)

    if output:
        fp.close()


if __name__ == "__main__":
    main()
