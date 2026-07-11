from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli 用 run() 関数（schema.json から自動生成）
# ---------------------------------------------------------
def run(loader_dir, output_file, schema_yaml):
    # schema.yaml 読み込み
    schema = read_yaml(schema_yaml)

    project = schema["project"]
    application = schema["application"]
    models = schema["models"]

    # ----------------------------------------
    # 1. Dashboard 用のクラス名 / インスタンス名を自動生成
    # ----------------------------------------
    site_class_name = f"{project.capitalize()}Dashboard"
    site_instance_name = f"{project.lower()}_dashboard"
    site_url_name = f"{project.lower()}_dashboard"

    # ----------------------------------------
    # 2. Dashboard のタイトルを自動生成
    # ----------------------------------------
    site_header = f"{project.capitalize()} Dashboard"
    site_title = f"{project.capitalize()} Dashboard"
    index_title = "Dashboard"

    # ----------------------------------------
    # 3. dashboard_models を schema.json の load_order から抽出
    #    ★ 依存関係順でモデル登録するために必須
    # ----------------------------------------
    load_order = schema.get("load_order", [])

    dashboard_models = [{"name": model_name} for model_name in load_order]

    # ----------------------------------------
    # Jinja2
    # ----------------------------------------
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template("dashboard.py.j2")

    # ----------------------------------------
    # テンプレートレンダリング
    # ----------------------------------------
    content = template.render(
        project=project,
        application=application,
        site_class_name=site_class_name,
        site_instance_name=site_instance_name,
        site_header=site_header,
        site_title=site_title,
        index_title=index_title,
        site_url_name=site_url_name,
        dashboard_models=dashboard_models,
    )

    # ----------------------------------------
    # 出力
    # ----------------------------------------
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content)

    print(f"[amcli] Generated dashboard: {out_path}")
