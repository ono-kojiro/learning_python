#!/usr/bin/env python3

import sys
import re

import getopt

import yaml
import random
import string

def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")

def read_yaml(filepath):
    fp = open(filepath, mode="r", encoding="utf-8")
    data = yaml.safe_load(fp)
    fp.close()
    return data

def random_string(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_random_cidr_ipv4(prefix=24):
    """
    192.168.X.Y/prefix の形式でランダム IPv4 CIDR を生成する
    """
    x = random.randint(0, 255)
    y = random.randint(1, 254)
    return f"192.168.{x}.{y}/{prefix}"

def generate_jsonfield_value(field_name, field_def):
    default = field_def.get("default", None)

    # addresses → CIDR のリスト
    if field_name == "addresses":
        return [generate_random_cidr_ipv4()]

    # dns → DNS のリスト
    if field_name == "dns":
        return [generate_random_dns()]

    # default=list
    if default == "list":
        return []

    # default=dict
    if default == "dict":
        return {}

    # fallback
    return []

def generate_random_dns():
    """
    ランダムな DNS アドレスを生成する（例: 8.8.8.X）
    """
    return f"8.8.8.{random.randint(1, 254)}"

def generate_random_value(model, field_name, field_def):
    ftype = field_def["type"]
    null_ok = field_def.get("null", False)
    default = field_def.get("default", None)

    # JSONField は専用関数に委譲
    if ftype == "JSONField":
        return generate_jsonfield_value(field_name, field_def)

    # CharField
    if ftype == "CharField":
        prefix = f"{model.upper()}-"
        return random_string(prefix)

    # GenericIPAddressField
    if ftype == "GenericIPAddressField":
        return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

    # ForeignKey
    if ftype == "ForeignKey":
        return None if null_ok else 1

    # null=True の場合のみ null を許可
    if null_ok:
        return None

    return random_string("VAL-")

def main():
    ret = 0

    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "hvo:c:",
            [
                "help",
                "version",
                "output=",
                "count=",
            ],
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None
    count = 10

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg
        elif option in ("-c", "--count"):
            count = int(optarg)
        else:
            assert False, "unknown option"

    if output is not None :
        fp = open(output, mode="w", encoding="utf-8")
    else :
        fp = sys.stdout

    if ret != 0:
        sys.exit(ret)

    fixtures = []

    for filepath in args:
        data = read_yaml(filepath)

        model = data['name']
        fields = data['fields']

        i = 1
        while i <= count:
            # 1件だけランダムデータを生成
            item = {
                "model": f"myapp.{model.lower()}",
                "pk": i,
                "fields": {}
            }

            for fname, field_def in fields.items():
                value = generate_random_value(model, fname, field_def)
                item["fields"][fname] = value

            fixtures.append(item)
            i += 1

    # YAML として出力
    fp.write('---\n')
    yaml.dump(fixtures, fp, allow_unicode=True, sort_keys=False)

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

