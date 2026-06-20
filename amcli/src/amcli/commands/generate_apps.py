from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli 用 run() 関数（テンプレート名は固定）
# ---------------------------------------------------------
def run(loader_dir, output_file, app_name, schema_path):
    TEMPLATE_NAME = "apps.py.j2"   # ★ 決め打ち

    # schema.json / schema.yaml を読み込む（今は使わないが将来拡張用）
    _schema = read_yaml(schema_path)

    # AppConfig クラス名
    app_class = app_name.capitalize() + "Config"

    # Jinja2
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template(TEMPLATE_NAME)

    # テンプレートレンダリング
    content = template.render(
        app_name=app_name,
        app_class=app_class,
    )

    # 出力
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content + "\n")

    print(f"[amcli] Generated apps.py: {out_path}")

