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

def random_human_name():
    first_names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve",
        "Frank", "Grace", "Hank", "Ivy", "Jack",
        "Karen", "Leo", "Mia", "Nina", "Oscar",
        "Paul", "Quinn", "Rose", "Sam", "Tina",
        "Uma", "Vince", "Wendy", "Xavier", "Yuki", "Zoe"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
        "Anderson", "Thomas", "Taylor", "Moore", "Jackson",
        "Martin", "Lee", "Perez", "Thompson", "White"
    ]

    return random.choice(first_names) + " " + random.choice(last_names)

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
    #if field_name == "addresses":
    #    cidr = generate_random_cidr_ipv4()
    #    return [cidr]

    # addresses → CIDR のリスト（複数生成に対応）
    if field_name == "addresses":
        # 80% の確率で 1 個、20% の確率で 2〜4 個
        if random.random() < 0.5:
            count = 1
        else:
            count = random.randint(2, 4)

        return [generate_random_cidr_ipv4() for _ in range(count)]
    
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

def generate_gateway_from_cidr(cidr):
    """
    192.168.X.Y/24 → 192.168.X.1 を返す
    """
    ip, prefix = cidr.split("/")
    a, b, c, d = ip.split(".")
    return f"{a}.{b}.{c}.1"

def generate_random_value(model, field_name, field_def):
    ftype = field_def["type"]
    null_ok = field_def.get("null", False)
    default = field_def.get("default", None)

    if model == "Manager" and field_name == "name":
        return random_human_name()

    # JSONField は専用関数に委譲
    if ftype == "JSONField":
        return generate_jsonfield_value(field_name, field_def)

    # gateway の自動生成（addresses から計算）
    if field_name == "gateway":
        # 直前に生成した addresses を参照する必要がある
        # → generate_random_value では参照できないため、
        #    gateway は後でまとめて処理する
        return None  # 一旦 None を返す
    
    # CharField
    if ftype == "CharField":
        prefix = f"{model.upper()}-"
        return random_string(prefix)

    # GenericIPAddressField
    if ftype == "GenericIPAddressField":
        return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

    # ManyToManyField → 整数のリストを返す
    if ftype == "ManyToManyField":
        # 最低1つの関連オブジェクトを作る
        # ここでは pk=1〜5 の中からランダムに選ぶ
        count = random.randint(1, 3)  # 1〜3個の関連を作る
        return [random.randint(1, 5) for _ in range(count)]

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

            # gateway の後処理
            if "addresses" in item["fields"] and "gateway" in item["fields"]:
                addrs = item["fields"]["addresses"]
                if addrs:
                    item["fields"]["gateway"] = generate_gateway_from_cidr(addrs[0])

            fixtures.append(item)
            i += 1

    # YAML として出力
    fp.write('---\n')
    yaml.dump(fixtures, fp, allow_unicode=True, sort_keys=False)

    if output is not None:
        fp.close()

if __name__ == "__main__":
    main()

