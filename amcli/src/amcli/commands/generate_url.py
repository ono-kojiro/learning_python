from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli 用 run() 関数（テンプレート名は固定）
# ---------------------------------------------------------
def run(loader_dir, output_file, schema_yaml):
    TEMPLATE_NAME = "urls_template.j2"   # ★ 決め打ち

    # Jinja2 環境
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template(TEMPLATE_NAME)

    # schema.yaml を読み込む
    schema = read_yaml(schema_yaml)

    # モデル名一覧を取得
    models = list(schema["models"].keys())

    # テンプレートレンダリング
    content = template.render(
        models=models,
    )

    # 出力
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content + "\n")

    print(f"[amcli] Generated urls: {out_path}")

