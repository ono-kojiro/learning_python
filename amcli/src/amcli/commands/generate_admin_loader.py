from pathlib import Path
import yaml


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli 用 run() 関数
# ---------------------------------------------------------
def run(output_file, schema_path):
    schema = read_yaml(schema_path)
    models = schema.get("models", {})

    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write("# auto-generated admin loader\n")

        for name in models.keys():
            lower = name.lower()
            fp.write(f"from .admin.{lower}_admin import *\n")

    print(f"[amcli] Generated admin_loader: {out_path}")

