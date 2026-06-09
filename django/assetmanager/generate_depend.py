#!/usr/bin/env python3

import sys
import getopt
import yaml
from collections import defaultdict, deque


def usage():
    print(f"Usage : {sys.argv[0]} -o <output> <input>...")


# ---------------------------------------------------------
# 依存関係抽出（既存）
# ---------------------------------------------------------
def extract_depend(data):
    deps = []
    fields = data.get('fields', {})
    for field_name, field_def in fields.items():
        ftype = field_def.get('type')
        if ftype in ('ForeignKey', 'OneToOneField', 'ManyToManyField'):
            deps.append(field_def['to'])
    return deps

# ---------------------------------------------------------
# トポロジカルソート（新規追加）
# ---------------------------------------------------------
def topo_sort(dep_map):
    graph = defaultdict(list)
    indegree = defaultdict(int)

    # 初期化
    for model, parents in dep_map.items():
        indegree[model] = len(parents)
        for p in parents:
            graph[p].append(model)

    # 入次数0のノードから開始
    queue = deque([m for m, d in indegree.items() if d == 0])
    order = []

    while queue:
        m = queue.popleft()
        order.append(m)

        for child in graph[m]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    return order


# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main():
    try:
        options, args = getopt.getopt(
            sys.argv[1:], "hvo:", ["help", "version", "output="]
        )
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    output = None

    for option, optarg in options:
        if option == "-v":
            usage()
            sys.exit(1)
        elif option in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif option in ("-o", "--output"):
            output = optarg

    if not args:
        print("Error: YAML files must be specified")
        sys.exit(1)

    dep_map = {}

    # 依存関係抽出
    for filepath in args:
        with open(filepath, "r", encoding="utf-8") as fp_in:
            data = yaml.safe_load(fp_in)
            model = data["name"]
            deps = extract_depend(data)
            dep_map[model] = deps

    # トポロジカルソートで loaddata 順を決定
    load_order = topo_sort(dep_map)

    # 逆向き依存を生成
    reverse_map = {model: [] for model in dep_map}

    for model, parents in dep_map.items():
        for p in parents:
            reverse_map[p].append(model)

    # depend.yaml の出力
    result = {
        "dependencies": dep_map,
        "reverse_dependencies": reverse_map,
        "load_order": load_order,
    }

    yaml_text = yaml.dump(result, sort_keys=True, allow_unicode=True)

    if output:
        with open(output, "w", encoding="utf-8") as fp:
            fp.write("---\n")
            fp.write(yaml_text)
    else:
        print("---")
        print(yaml_text)


if __name__ == "__main__":
    main()
