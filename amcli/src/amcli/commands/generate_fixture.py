from pathlib import Path
import yaml
import random
import string
from collections import defaultdict, deque
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# 名前生成（外部 YAML）
# ---------------------------------------------------------
def random_human_name(name_data):
    first = name_data.get("first_names", [])
    last = name_data.get("last_names", [])
    if not first or not last:
        return "Unknown User"
    return random.choice(first) + " " + random.choice(last)


# ---------------------------------------------------------
# ランダム値生成
# ---------------------------------------------------------
def random_string(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


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


def generate_random_value(model, field_name, field_def, count, pk, name_data):
    ftype = field_def["type"]
    null_ok = field_def.get("null", False)

    if model == "Manager" and field_name == "name":
        return random_human_name(name_data)

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


# ---------------------------------------------------------
# 依存関係
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# amcli 用 run() 関数
# ---------------------------------------------------------
def run(loader_dir, output_file, schema_yaml, names_yaml, ref_yaml_list, count=10, include_deps=False):
    # schema.yaml
    schema = read_yaml(schema_yaml)
    dependencies = schema["dependencies"]

    # 名前テンプレート
    name_data = read_yaml(names_yaml) if names_yaml else {"first_names": [], "last_names": []}

    # *_ref.yaml 読み込み
    models = {}
    target_models = []

    for filepath in ref_yaml_list:
        data = read_yaml(filepath)
        model = data["name"]
        models[model] = data["fields"]
        target_models.append(model)

    # 依存モデル
    deps = collect_dependencies(target_models, dependencies)

    if include_deps:
        generate_models = list(set(target_models) | deps)
    else:
        generate_models = target_models

    # 依存順
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

    # Jinja2
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template("fixture_template.j2")

    content = template.render(fixtures=fixtures)

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content)

    print(f"[amcli] Generated fixture: {out_path}")

