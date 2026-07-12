# src/amcli/commands/cmp2ref/pk.py

from .convert import convert_primitive_field

def get_pk_field(models, model_name):
    fields = models[model_name]["fields"]

    # unique=True のフィールドを PK とみなす（最新仕様）
    for fname, fdef in fields.items():
        if fdef.get("unique", False):
            return fname, convert_primitive_field(fdef)

    return None, None

