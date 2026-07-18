# src/amcli/commands/generate_fixture/loader.py

import os
import yaml
from amcli.utils.debug import debug

def load_models(schema_yaml):
    with open(schema_yaml, "r", encoding="utf-8") as fp:
        schema = yaml.safe_load(fp)

    models_raw = schema["models"]

    models = {}
    for k, v in models_raw.items():
        if "fields" in v:
            models[k.lower()] = v["fields"]
        else:
            models[k.lower()] = v

    debug(f"[DEBUG] models keys AFTER flatten: {list(models.keys())}")
    return models

def load_testschema(testschema_yaml):
    with open(testschema_yaml, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)

def load_names(names_yaml):
    with open(names_yaml, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)

def load_dependencies(ref_yaml_list):
    deps = []
    for ref in ref_yaml_list:
        if os.path.isdir(ref):
            continue
        with open(ref, "r", encoding="utf-8") as fp:
            deps.append(yaml.safe_load(fp))
    return deps

