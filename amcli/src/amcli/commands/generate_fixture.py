# src/amcli/commands/generate_fixture.py

from pathlib import Path
import yaml

from amcli.utils.constants import normalize_field_type
from amcli.utils.fixture_builder import build_fixtures
from amcli.utils.fixture_renderer import render_fixtures


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def run(loader_dir, output_file, schema_yaml, names_yaml, ref_yaml_list, count=10, include_deps=False):
    schema = read_yaml(schema_yaml)
    dependencies = schema["dependencies"]

    name_data = read_yaml(names_yaml) if names_yaml else {"first_names": [], "last_names": []}

    models = {}

    for filepath in ref_yaml_list:
        data = read_yaml(filepath)
        model = data["name"]

        for fname, fdef in data["fields"].items():
            fdef["type"] = normalize_field_type(fdef["type"])

        models[model] = data["fields"]

    fixtures = build_fixtures(models, dependencies, name_data, count, include_deps)

    render_fixtures(loader_dir, output_file, fixtures)
