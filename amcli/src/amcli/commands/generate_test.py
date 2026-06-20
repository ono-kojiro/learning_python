# src/amcli/commands/generate_test.py

from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)

def run(schema_yaml, ref_yaml, output_file):
    schema = read_yaml(schema_yaml)
    meta_models = schema["models"]

    data = read_yaml(ref_yaml)
    model = data["name"]
    fields = meta_models[model]["fields"]

    env = Environment(
        loader=FileSystemLoader("template"),
        autoescape=False
    )
    env.filters["repr"] = repr

    template = env.get_template("test_generated.j2")

    content = template.render(
        model=model,
        model_lower=model.lower(),
        fields=fields,
        fields_json=repr(fields),
    )

    Path(output_file).write_text(content + "\n", encoding="utf-8")

    print(f"[amcli] Generated test: {output_file}")

