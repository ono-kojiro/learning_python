from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli generate_importer（テンプレート主導・複数テンプレート→1ファイル）
# ---------------------------------------------------------
def run(output_file, schema_path, template_files):
    # schema.json 読み込み（任意）
    schema = read_yaml(schema_path) if schema_path else {}
    models = list(schema.get("models", {}).keys())
    application = schema.get("application")
    project = schema.get("project")

    # apps.py 用
    app_class = None
    if application:
        app_class = application.capitalize() + "Config"

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        for tmpl_path in template_files:
            tmpl_path = Path(tmpl_path)
            loader_dir = tmpl_path.parent
            template_name = tmpl_path.name

            env = Environment(
                loader=FileSystemLoader(loader_dir),
                autoescape=False
            )
            template = env.get_template(template_name)

            # 区切りコメント
            fp.write(f"# --- from {template_name} ---\n")

            # レンダリング
            content = template.render(
                models=models,
                application=application,
                project=project,
                app_class=app_class,
            )

            fp.write(content)
            fp.write("\n\n")

    print(f"[amcli] Generated importer: {out_path}")

