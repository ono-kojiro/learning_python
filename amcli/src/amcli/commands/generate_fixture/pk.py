# src/amcli/commands/generate_fixture/pk.py

def find_pk_field(model, fields):
    pk_field = None

    # primary_key があれば最優先
    for fname, fdef in fields.items():
        if fdef.get("primary_key", False):
            return fname

    # unique=True も PK とみなす（cmp2ref の新仕様）
    for fname, fdef in fields.items():
        if fdef.get("unique", False):
            return fname

    raise ValueError(f"Model {model} に primary_key がありません")

