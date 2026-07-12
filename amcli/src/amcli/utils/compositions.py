# amcli/utils/compositions.py

import os
import sys
import json

from amcli.utils.debug import debug

#DEBUG = os.environ.get("VERBOSE", "0") != "0"
DEBUG = True

def collect_compositions(models):
    compositions = {}

    debug("=== collect_compositions DEBUG START ===")

    # 親側の所有痕跡（JSONField / OneToOneField）
    for parent, model_def in models.items():
        debug(f"\n[DEBUG] Parent model: {parent}")
        children = []

        for fname, fdef in model_def["fields"].items():
            ftype = fdef["type"]
            debug(f"  Field: {fname}, type={ftype}, def={fdef}")

            # 親側の OneToOneField（所有）
            if ftype == "OneToOneField":
                to = fdef.get("to")
                if to:
                    if parent < to:
                        debug(f"    -> OneToOneField OWNERSHIP: parent={parent}, child={to}")
                        children.append(to)
                    else:
                        debug(f"    -> OneToOneField REVERSE REF (ignored): {parent}.{fname} -> {to}")

            # JSONField（OneToMany の親側痕跡）
            if ftype == "JSONField":
                help_text = fdef.get("help_text", "")
                debug(f"    -> JSONField help_text={help_text}")
                if help_text.startswith("Owned children of "):
                    child = help_text.replace("Owned children of ", "")
                    debug(f"    -> OneToMany detected: parent={parent}, child={child}")
                    children.append(child)

        if children:
            compositions[parent] = children
            debug(f"[DEBUG] Parent {parent} owns children: {children}")
        else:
            debug(f"[DEBUG] Parent {parent} owns no children")

    # 子側の ForeignKey（所有の実体）
    debug("\n=== Reverse FK scan ===")
    for child, model_def in models.items():
        for fname, fdef in model_def["fields"].items():
            if fdef["type"] == "ForeignKey":
                parent = fdef.get("to")
                debug(f"  Reverse FK: child={child} -> parent={parent}")
                if parent:
                    compositions.setdefault(parent, [])
                    if child not in compositions[parent]:
                        compositions[parent].append(child)
                        debug(f"    -> Added ownership: {parent} owns {child}")

    debug("\n=== collect_compositions DEBUG END ===")
    debug(f"Final compositions: {compositions}\n")

    return compositions


def find_composition_root(compositions):
    """
    Composition Model の root を自動判定する。
    「子として一度も登場しないモデル」が root。

    Device 特別扱いなし。
    図書館システムでも Book, Shelf, Library などに自動適用可能。
    """

    children = set()
    for child_list in compositions.values():
        for child in child_list:
            children.add(child)

    # 親のうち子に含まれていないモデルが root
    roots = [parent for parent in compositions.keys() if parent not in children]

    return roots[0] if roots else None


def build_load_order_from_compositions(compositions, root):
    order = []
    visited = set()

    print("=== build_load_order_from_compositions start ===")
    print(json.dumps(compositions, indent=2))

    print("=== root ===")
    print(root)

    print("=== compositions.get(root) ===")
    print(compositions.get(root))

    def dfs(model):
        if model in visited:
            return
        visited.add(model)
        for child in compositions.get(model, []):
            dfs(child)
        order.append(model)

    dfs(root)

    print("=== build_load_order_from_compositions end ===")

    return order
