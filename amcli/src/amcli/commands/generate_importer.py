from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli generate_importer（テンプレートを1つずつ処理して append）
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

    # 出力ファイルを最初に空にする
    out_path.write_text("", encoding="utf-8")

    # テンプレートを1つずつ処理
    for tmpl_path in template_files:
        tmpl_path = Path(tmpl_path)
        loader_dir = tmpl_path.parent
        template_name = tmpl_path.name

        # Jinja2 loader はテンプレートごとに切り替える
        env = Environment(
            loader=FileSystemLoader(loader_dir),
            autoescape=False
        )
        template = env.get_template(template_name)

        # レンダリング
        content = template.render(
            models=models,
            application=application,
            project=project,
            app_class=app_class,
        ).rstrip()

        # 出力へ append
        with open(out_path, "a", encoding="utf-8") as fp:
            fp.write(f"# --- from {template_name} ---\n\n")
            fp.write(content)
            fp.write("\n\n")  # テンプレート間の区切り

    print(f"[amcli] Generated importer: {out_path}")
