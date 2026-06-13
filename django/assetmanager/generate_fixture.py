#!/usr/bin/env python3

import sys
import getopt
import yaml
import random
import string


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")


def read_yaml(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def random_string(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_human_name():
    first_names = [
        "Alice","Bob","Charlie","Diana","Eve","Frank","Grace","Hank","Ivy","Jack",
        "Karen","Leo","Mia","Nina","Oscar","Paul","Quinn","Rose","Sam","Tina",
        "Uma","Vince","Wendy","Xavier","Yuki","Zoe"
    ]
    last_names = [
        "Smith","Johnson","Williams","Brown","Jones","Miller","Davis","Garcia",
        "Rodriguez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson",
        "Martin","Lee","Perez","Thompson","White"
    ]
    return random.choice(first_names) + " " + random.choice(last_names)


def generate_random_cidr_ipv4(prefix=24):
    x = random.randint(0, 255)
    y = random.randint(1, 254)
    return f"192.168.{x}.{y}/{prefix}"


def generate_jsonfield_value(field_name, field_def):
    default = field_def.get("default", None)

    if field_name == "addresses":
        count = 1 if random.random() < 0.5 else random.randint(2, 4)
        return [generate_random_cidr_ipv4() for _ in range(count)]

    if field_name == "dns":
        return [f"8.8.8.{random.randint(1, 254)}"]

    if default == "list":
        return []

    if default == "dict":
        return {}

    return []


def generate_gateway_from_cidr(cidr):
    ip, prefix = cidr.split("/")
    a, b, c, d = ip.split(".")
    return f"{a}.{b}.{c}.1"


def generate_random_value(model, field_name, field_def, count):
    ftype = field_def["type"]
    null_ok = field_def.get("null", False)

    # Manager.name は人名にする
    if model == "Manager" and field_name == "name":
        return random_human_name()

    # JSONField
    if ftype == "JSONField":
        return generate_jsonfield_value(field_name, field_def)

    # gateway は後で addresses から計算
    if field_name == "gateway":
        return None

    # CharField
    if ftype == "CharField":
        prefix = f"{model.upper()}-"
        return random_string(prefix)

    # IP アドレス
    if ftype == "GenericIPAddressField":
        return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

    # ForeignKey → 1〜count のどれかを参照（暫定）
    if ftype == "ForeignKey":
        # null=True の場合だけ None を許可
        if null_ok and random.random() < 0.2:
            return None
        # 1〜count の整数（＝参照先の pk を想定）
        return random.randint(1, count)

    # ManyToManyField → 1〜count の整数リスト（暫定）
    if ftype == "ManyToManyField":
        # 1〜3 個の関連を作る
        n = random.randint(1, min(3, count))
        # 重複なしで選ぶ
        return random.sample(list(range(1, count + 1)), n)

    # null=True の場合のみ None を許可
    if null_ok:
        return None

    # その他は適当な文字列
    return random_string("VAL-")


def main():
    options, args = getopt.getopt(
        sys.argv[1:], "hvo:c:", ["help", "version", "output=", "count="]
    )

    output = None
    count = 10

    for option, optarg in options:
        if option in ("-o", "--output"):
            output = optarg
        elif option in ("-c", "--count"):
            count = int(optarg)

    fp = open(output, "w", encoding="utf-8") if output else sys.stdout

    fixtures = []

    for filepath in args:
        data = read_yaml(filepath)
        model = data["name"]
        fields = data["fields"]

        for i in range(1, count + 1):
            item = {
                "model": f"myapp.{model.lower()}",
                "pk": i,          # ★ pk は単純に 1..count
                "fields": {}
            }

            # まず全フィールド生成
            for fname, field_def in fields.items():
                value = generate_random_value(model, fname, field_def, count)
                item["fields"][fname] = value

            # gateway の後処理
            if "addresses" in item["fields"] and "gateway" in item["fields"]:
                addrs = item["fields"]["addresses"]
                if addrs:
                    item["fields"]["gateway"] = generate_gateway_from_cidr(addrs[0])

            fixtures.append(item)

    fp.write("---\n")
    yaml.dump(fixtures, fp, allow_unicode=True, sort_keys=False)

    if output:
        fp.close()


if __name__ == "__main__":
    main()
