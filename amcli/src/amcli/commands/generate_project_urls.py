from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

def read_yaml(filepath):
    with open(filepath, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)

def run(loader_dir, output_file, schema_yaml):
    schema = read_yaml(schema_yaml)

    project = schema["project"]
    application = schema["application"]

    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template("project_urls.py.j2")

    content = template.render(
        project=project,
        application=application,
    )

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content)

    print(f"[amcli] Generated project urls.py: {out_path}")

