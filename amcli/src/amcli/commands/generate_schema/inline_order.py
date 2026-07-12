# src/amcli/commands/generate_schema/inline_order.py

def topo_sort_inline(nested, root):
    graph = {}

    for parent, children in nested.items():
        graph[parent] = []
        for item in children:
            model = item.get("model")
            if model:
                graph[parent].append(model)

    visited = set()
    order = []

    def dfs(model):
        if model in visited:
            return
        visited.add(model)
        for child in graph.get(model, []):
            dfs(child)
        order.append(model)

    if root:
        dfs(root)

    return order

