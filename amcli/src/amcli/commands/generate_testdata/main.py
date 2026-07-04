import os
import json
import datetime

DEBUG = True

# ============================================================
# Utility
# ============================================================

def ensure_outdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_schema(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_ref_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def gen_dummy_value(fname, fdef):
    ftype = fdef.get("type")

    # ★ ID を含めないため、PrimaryKey は生成しない
    if ftype == "AutoField":
        return None

    if ftype == "CharField":
        return f"{fname.upper()}-{os.urandom(4).hex()}"

    if ftype == "IntegerField":
        return 1

    if ftype == "DateTimeField":
        return datetime.datetime.now().isoformat()

    if ftype == "JSONField":
        return {}

    return None

# ============================================================
# Dependency expansion
# ============================================================

def expand_dependencies(schema, model_name):
    deps = schema["dependencies"].get(model_name, [])
    expanded = []
    for d in deps:
        expanded.extend(expand_dependencies(schema, d))
        expanded.append(d)
    uniq = []
    for x in expanded:
        if x not in uniq:
            uniq.append(x)
    return uniq

def get_dependency_order(schema, model_names):
    ordered = []
    for m in model_names:
        deps = expand_dependencies(schema, m)
        for d in deps:
            if d not in ordered:
                ordered.append(d)
        if m not in ordered:
            ordered.append(m)
    return ordered

# ============================================================
# JSON generator
# ============================================================

def gen_json(model_name, fields_def, outdir, index):
    """
    Pure JSON body for curl POST.
    ID を含めない。FK は *_id に変換して null を入れる。
    M2M は *_ids に変換して空配列を入れる。
    """
    body = {}

    for fname, fdef in fields_def.items():

        # ★ ID を含めない
        if fname == "id":
            continue

        ftype = fdef["type"]

        # ★ ForeignKey → *_id に変換
        if ftype == "ForeignKey":
            body[f"{fname}_id"] = None
            continue

        # ★ OneToOneField → フィールド名そのまま
        if ftype == "OneToOneField":
            body[fname] = None
            continue

        # ★ ManyToMany → *_ids に変換
        if ftype == "ManyToManyField":
            body[f"{fname}_ids"] = []
            continue

        # ★ 通常フィールド
        body[fname] = gen_dummy_value(fname, fdef)

    fname = f"{index:03d}_{model_name.lower()}.json"
    path = os.path.join(outdir, fname)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(body, f, indent=2, ensure_ascii=False)
        f.write("\n")  # 末尾改行

    if DEBUG:
        print(f"[DEBUG] wrote {path}")

# ============================================================
# Entry point called from cli.py
# ============================================================

def run(schema_path, outdir, ref_json_paths):
    """
    Main entry point for gentestdata command.
    Only ADD phase is generated.
    ID を含めないテストデータを生成する。
    """
    ensure_outdir(outdir)

    schema = load_schema(schema_path)
    refs = [load_ref_json(p) for p in ref_json_paths]
    model_names = [r["name"] for r in refs]

    # ADD のみなので依存関係展開は必須
    ordered_models = get_dependency_order(schema, model_names)

    if DEBUG:
        print("[DEBUG] dependency order =", ordered_models)

    index = 1

    # -------------------------
    # ADD phase only
    # -------------------------
    for m in ordered_models:
        fields_def = next(r["fields"] for r in refs if r["name"] == m)
        gen_json(m, fields_def, outdir, index)
        index += 1
