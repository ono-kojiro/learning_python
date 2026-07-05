# src/amcli/utils/fixture_renderer.py

from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def render_fixtures(loader_dir, output_file, fixtures):
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

