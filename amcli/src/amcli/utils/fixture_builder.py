# src/amcli/utils/fixture_builder.py

from collections import defaultdict, deque
from amcli.utils.random_generators import (
    generate_random_value,
    generate_gateway_from_cidr,
)


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
    result = set()

    def dfs(model):
        for dep in dependencies.get(model, []):
            if dep not in result:
                result.add(dep)
                dfs(dep)

    for t in targets:
        dfs(t)

    return result


def build_fixtures(models, dependencies, name_data, count, include_deps):
    target_models = list(models.keys())
    deps = collect_dependencies(target_models, dependencies)

    if include_deps:
        generate_models = list(set(target_models) | deps)
    else:
        generate_models = target_models

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
                item["fields"][fname] = generate_random_value(
                    model, fname, fdef, count, pk, name_data
                )

            if "addresses" in item["fields"] and "gateway" in item["fields"]:
                addrs = item["fields"]["addresses"]
                if addrs:
                    item["fields"]["gateway"] = generate_gateway_from_cidr(addrs[0])

            fixtures.append(item)

    return fixtures

