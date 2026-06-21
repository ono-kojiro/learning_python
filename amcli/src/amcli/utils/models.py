from .io import read_json

def collect_models(ref_files):
    models = {}
    for path in ref_files:
        data = read_json(path)
        name = data["name"]
        fields = data.get("fields", {})
        models[name] = {"fields": fields}
    return models

