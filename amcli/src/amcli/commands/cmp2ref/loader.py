# src/amcli/commands/cmp2ref/loader.py

import yaml

def load_owner_models(paths):
    models = {}
    for path in paths:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            models.update(data)
    return models

