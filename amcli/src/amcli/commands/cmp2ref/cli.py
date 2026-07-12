# src/amcli/commands/cmp2ref/cli.py

from pathlib import Path
import json

from .loader import load_owner_models
from .builder import build_reference_model

def run(spec, output_file, input_files):
    cmp_paths = [Path(f).resolve() for f in input_files]

    spec_path = Path(spec)
    stem = spec_path.stem
    target_lower = stem.lower()

    models = load_owner_models(cmp_paths)
    yaml_keys = list(models.keys())

    target_model = None
    for key in yaml_keys:
        if key.lower() == target_lower:
            target_model = key
            break

    if target_model is None:
        print(f"[amcli] ERROR: Model '{stem}' not found in YAML keys: {yaml_keys}")
        raise RuntimeError(f"Model '{stem}' not found")

    result = build_reference_model(models, target_model)

    output_path = Path(output_file).resolve()

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"[amcli] Generated: {output_path}")

