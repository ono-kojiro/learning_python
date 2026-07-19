# file: src/amcli/commands/generate_schema/primary_key.py

def collect_primary_keys(models):
    """
    schema.json に primary_key 情報を追加するための抽出処理。
    入力 models は変更しない。
    ルール：xxx_id + unique=true → primary_key=true
    """
    pk_map = {}

    for model_name, model_def in models.items():
        fields = model_def.get("fields", {})
        for fname, fdef in fields.items():
            if fname.endswith("_id") and fdef.get("unique", False):
                pk_map[model_name] = fname

    return pk_map
