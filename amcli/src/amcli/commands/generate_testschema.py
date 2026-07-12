# src/amcli/commands/generate_testschema.py

import json
from pathlib import Path
from collections import defaultdict, deque


# ============================================================
# 1. schema.json の読み込み
# ============================================================
def load_schema(schema_path):
    schema_file = Path(schema_path)
    if not schema_file.exists():
        raise FileNotFoundError(f"schema.json not found: {schema_path}")

    with open(schema_file, "r", encoding="utf-8") as fp:
        return json.load(fp)


# ============================================================
# 2. build_order の生成（旧 load_order）
# ============================================================
def build_build_order(schema):
    """
    build_order は API の登録順（POST 順）
    schema.json の load_order をそのまま使う
    """
    order = schema.get("load_order")
    if not order:
        raise ValueError("schema.json に load_order がありません")
    return order


# ============================================================
# 3. delete_order の生成（build_order の逆順）
# ============================================================
def build_delete_order(build_order):
    return [m.lower() for m in reversed(build_order)]


# ============================================================
# 4. 依存関係グラフの構築
# ============================================================
def build_dependency_graph(schema):
    """
    dependencies = {
        "Device": ["Comment", "Remark"],
        "NetIF": ["Device"],
        ...
    }
    """
    return schema.get("dependencies", {})


# ============================================================
# 5. トポロジカルソート（依存関係順）
# ============================================================
def topological_sort(dependencies):
    indegree = defaultdict(int)
    graph = defaultdict(list)

    # 親 → 子 のグラフを構築
    for model, parents in dependencies.items():
        for p in parents:
            graph[p].append(model)
            indegree[model] += 1

    # 入次数 0 のノードから開始
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


# ============================================================
# 6. load_order の生成（旧 loaddata_order）
# ============================================================
def build_load_order(schema):
    """
    load_order は FK の依存関係順（参照される側 → 参照する側）
    dependencies を使って topological_sort で生成する
    """
    dependencies = build_dependency_graph(schema)
    order = topological_sort(dependencies)
    return [m.lower() for m in order]

def topo_sort(model_names, dependencies):
    visited = set()
    result = []

    def visit(model):
        model_l = model.lower()

        if model_l in visited:
            return
        visited.add(model_l)

        # 依存先（FK 参照先）を先に visit する
        for dep in dependencies.get(model, []):
            visit(dep)

        # 自分自身を追加
        result.append(model_l)

    # schema["models"].keys() は大文字なのでそのまま使う
    for model in model_names:
        visit(model)

    return result

# ============================================================
# 7. メイン処理
# ============================================================
def run(schema_path, output_path):
    schema = load_schema(schema_path)

    build_order = build_build_order(schema)
    delete_order = build_delete_order(build_order)

    fixture_order = topo_sort(schema["models"].keys(), schema["dependencies"])

    test_schema = {
        "build_order": build_order,
        "delete_order": delete_order,
        "fixture_order": fixture_order,
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(test_schema, fp, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated test_schema: {out_file}")



