from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def run(loader_dir, output_file, ref_yaml):
    TEMPLATE_NAME = "viewset_template.j2"

    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template(TEMPLATE_NAME)

    data = read_yaml(ref_yaml)
    model = data["name"]

    # ★ 主キー候補（xxx_id）を抽出
    pk_field = None
    for fname in data.get("fields", {}):
        if fname.endswith("_id"):
            pk_field = fname
            break

    # テンプレート展開
    content = template.render(
        model=model,
        model_lower=model.lower(),
        pk_field=pk_field,
        depth_param=True,   # ★ 追加：テンプレート側で depth を動的に扱うため
    )

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content + "\n")

    print(f"[amcli] Generated view: {out_path}")
