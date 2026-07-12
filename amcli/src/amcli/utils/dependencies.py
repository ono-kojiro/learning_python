# amcli/utils/dependencies.py

from collections import defaultdict, deque
from amcli.utils.constants import FieldType, normalize_field_type


def collect_dependencies(models):
    """
    モデルの fields を走査して依存関係を抽出する。
    ForeignKey / OneToOneField / ManyToManyField を対象とする。
    """
    deps = {m: [] for m in models}

    for model, data in models.items():
        for fname, fdef in data["fields"].items():
            ftype = normalize_field_type(fdef.get("type"))
            to = fdef.get("to")

            if ftype in (
                FieldType.FOREIGN_KEY,
                FieldType.ONE_TO_ONE,
                FieldType.MANY_TO_MANY,
            ):
                if to:
                    deps[model].append(to)

    return deps


def collect_all_dependencies(deps):
    """
    依存関係の transitive closure（全依存）を求める。
    """
    all_deps = {}

    for model in deps.keys():
        visited = set()
        stack = list(deps[model])

        while stack:
            m = stack.pop()
            if m not in visited:
                visited.add(m)
                stack.extend(deps.get(m, []))

        all_deps[model] = list(visited)

    return all_deps


def build_reverse_dependencies(dependencies):
    reverse = {model: [] for model in dependencies.keys()}

    for model, deps in dependencies.items():
        for dep in deps:
            # dep を参照しているのは model なので
            reverse[dep].append(model)

    return reverse

def topo_sort(dep_map):
    """
    トポロジカルソート。
    """
    graph = defaultdict(list)
    indegree = defaultdict(int)

    for model, parents in dep_map.items():
        indegree[model] = len(parents)
        for p in parents:
            graph[p].append(model)

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
