import os
from pathlib import Path
import yaml
import json
from jinja2 import Environment, FileSystemLoader


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)

def compute_fk_create_order(model_name, schema):
    deps = schema["dependencies"].get(model_name, [])
    load_order = schema["load_order"]

    # load_order の順番を維持しつつ、依存モデルだけを抽出
    ordered = [m for m in load_order if m in deps]
    return ordered

def run(schema_yaml, ref_yaml, template_file, output_file):
    # --- ref.yaml（テスト対象モデル） ---
    data = read_yaml(ref_yaml)
    model = data["name"]
    fields = data["fields"]

    # --- schema.json ---
    schema = read_yaml(schema_yaml)

    # SSOT から必要な情報を取得
    load_order = schema["load_order"]
    all_dependencies = schema["all_dependencies"]          # ★ 全依存（transitive）
    reverse_dependencies = schema["reverse_dependencies"]  # ★ 逆方向依存
    dependencies = schema["dependencies"]                  # ★ 直接依存（Borrow → User, Book）

    # このモデルが依存する全モデル（Device → NetIF → IPv4 など）
    deps = all_dependencies.get(model, [])

    # load_order に従って FK 作成順序を決定
    fk_create_order = compute_fk_create_order(model, schema)

    # --- Jinja2 テンプレート ---
    env = Environment(
        loader=FileSystemLoader(os.path.dirname(template_file)),
        autoescape=False
    )
    env.filters["repr"] = repr

    template = env.get_template(os.path.basename(template_file))

    # --- テンプレートへ埋め込む ---
    content = template.render(
        model=model,
        model_lower=model.lower(),
        fields=fields,
        fields_json=repr(fields),
        fk_create_order=fk_create_order,
        reverse_deps=reverse_dependencies,
        dependencies=dependencies,            # ★ 追加：テンプレートで使える
        all_dependencies=all_dependencies,    # ★ 追加：テンプレートで使える
        load_order=load_order                 # ★ 追加：テンプレートで使える
    )

    # --- 出力 ---
    Path(output_file).write_text(content + "\n", encoding="utf-8")
    print(f"[amcli] Generated test: {output_file}")
