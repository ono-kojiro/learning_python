#!/usr/bin/env python3

import sys
import getopt
import yaml
import random
import string
from collections import defaultdict, deque


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def random_string(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_human_name():
    first = ["Alice","Bob","Charlie","Diana","Eve","Frank","Grace","Hank","Ivy","Jack",
             "Karen","Leo","Mia","Nina","Oscar","Paul","Quinn","Rose","Sam","Tina",
             "Uma","Vince","Wendy","Xavier","Yuki","Zoe"]
    last = ["Smith","Johnson","Williams","Brown","Jones","Miller","Davis","Garcia",
            "Rodriguez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson",
            "Martin","Lee","Perez","Thompson","White"]
    return random.choice(first) + " " + random.choice(last)


def generate_random_cidr_ipv4(prefix=24):
    x = random.randint(0, 255)
    y = random.randint(1, 254)
    return f"192.168.{x}.{y}/{prefix}"


def generate_jsonfield_value(field_name, field_def):
    default = field_def.get("default", None)

    if field_name == "addresses":
        count = random.randint(1, 4)
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


def generate_random_value(model, field_name, field_def, count, pk):
    ftype = field_def["type"]
    null_ok = field_def.get("null", False)

    if model == "Manager" and field_name == "name":
        return random_human_name()

    if ftype == "JSONField":
        return generate_jsonfield_value(field_name, field_def)

    if field_name == "gateway":
        return None

    if ftype == "CharField":
        return random_string(f"{model.upper()}-")

    if ftype == "GenericIPAddressField":
        return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

    if ftype == "OneToOneField":
        return pk

    if ftype == "ForeignKey":
        if null_ok and random.random() < 0.2:
            return None
        return random.randint(1, count)

    if ftype == "ManyToManyField":
        n = random.randint(1, min(3, count))
        return random.sample(list(range(1, count + 1)), n)

    if null_ok:
        return None

    return random_string("VAL-")


def topological_sort(dependencies):
    indegree = defaultdict(int)
    graph = defaultdict(list)

    for model, deps in dependencies.items():
        for d in deps:
            graph[d].append(model)
            indegree[model] += 1

    queue = deque([m for m in dependencies if indegree[m] == 0])
    order = []

    while queue:
        m = queue.popleft()
        order.append(m)
        for nxt in graph[m]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order


def collect_dependencies(targets, dependencies):
    """ターゲットモデルが依存するモデルをすべて集める"""
    result = set()

    def dfs(model):
        for dep in dependencies.get(model, []):
            if dep not in result:
                result.add(dep)
                dfs(dep)

    for t in targets:
        dfs(t)

    return result


def main():
    options, args = getopt.getopt(
        sys.argv[1:], "ho:m:c:", ["help", "output=", "meta=", "count=", "with-deps", "no-deps"]
    )

    output = None
    meta_path = None
    count = 10
    include_deps = False

    for opt, val in options:
        if opt in ("-o", "--output"):
            output = val
        elif opt in ("-m", "--meta"):
            meta_path = val
        elif opt in ("-c", "--count"):
            count = int(val)
        elif opt == "--with-deps":
            include_deps = True
        elif opt == "--no-deps":
            include_deps = False

    if not meta_path:
        print("ERROR: meta.yaml is required (-m)")
        return

    meta = read_yaml(meta_path)
    dependencies = meta["dependencies"]

    # *_ref.yaml を読み込む
    models = {}
    target_models = []

    for filepath in args:
        data = read_yaml(filepath)
        model = data["name"]
        models[model] = data["fields"]
        target_models.append(model)

    # 依存モデルを収集
    deps = collect_dependencies(target_models, dependencies)

    # 生成対象モデル
    if include_deps:
        generate_models = list(set(target_models) | deps)
    else:
        generate_models = target_models

    # 依存関係順に並べる
    order = topological_sort(dependencies)
    order = [m for m in order if m in generate_models]

    fixtures = []

    for model in order:
        fields = models[model]
        for pk in range(1, count + 1):
            item = {
                "model": f"myapp.{model.lower()}",
                "pk": pk,
                "fields": {}
            }

            for fname, fdef in fields.items():
                item["fields"][fname] = generate_random_value(model, fname, fdef, count, pk)

            if "addresses" in item["fields"] and "gateway" in item["fields"]:
                addrs = item["fields"]["addresses"]
                if addrs:
                    item["fields"]["gateway"] = generate_gateway_from_cidr(addrs[0])

            fixtures.append(item)

    fp = open(output, "w", encoding="utf-8") if output else sys.stdout
    fp.write("# Generated by generate_fixture.py\n---\n")
    yaml.dump(fixtures, fp, allow_unicode=True, sort_keys=False)
    if output:
        fp.close()


if __name__ == "__main__":
    main()
