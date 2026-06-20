from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli 用 run() 関数
# ---------------------------------------------------------
def run(loader_dir, output_file, template_j2, ref_yaml):
    # Jinja2 環境
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template(template_j2)

    # ref_yaml 読み込み
    data = read_yaml(ref_yaml)
    model = data["name"]

    # テンプレート展開
    content = template.render(
        model=model,
        model_lower=model.lower(),
    )

    # 出力
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content + "\n")

    print(f"[amcli] Generated view: {out_path}")

