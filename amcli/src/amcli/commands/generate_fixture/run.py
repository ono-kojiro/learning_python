import yaml
from .loader import load_models, load_testschema, load_names, load_dependencies
from .builder import build_fixtures

def run(loader_dir, output_file, schema_yaml, testschema_yaml, names_yaml, ref_yaml_list,
        count=10, include_deps=False):

    models = load_models(schema_yaml)
    testschema = load_testschema(testschema_yaml)
    name_data = load_names(names_yaml)
    dependencies = load_dependencies(ref_yaml_list)

    fixtures = build_fixtures(
        models=models,
        dependencies=dependencies,
        name_data=name_data,
        count=count,
        include_deps=include_deps,
        testschema=testschema,
    )

    with open(output_file, "w", encoding="utf-8") as fp:
        yaml.safe_dump(fixtures, fp, allow_unicode=True)

    print(f"[amcli] Generated fixture: {output_file}")

