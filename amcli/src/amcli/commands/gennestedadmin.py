import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def run(template_dir, output_file, schema_json):
    """
    schema.json の inline_order / nested を使って
    正しい階層構造の Inline クラスを生成する。
    DeviceAdmin の register は device_admin.py が担当する。
    """

    # schema.json を読み込み
    schema = json.load(open(schema_json))

    models = list(schema["models"].keys())  # ★ これが重要（models をテンプレートに渡す）

    nested = schema["nested"]
    inline_order = schema["inline_order"]  # ["IPv4", "NetIF", "OS", "Device"]

    # ------------------------------------------------------------
    # Inline クラスの構築
    # ------------------------------------------------------------
    inline_map = {}

    # まず model → Inline の基本形を作る
    for parent, children in nested.items():
        for item in children:
            model = item.get("model")
            if not model:
                continue

            inline_map[model] = {
                "class_name": f"{model}Inline",
                "model": model,
                "children": []
            }

    # 子 Inline を追加（NetIF → IPv4 など）
    for parent, children in nested.items():
        for item in children:
            model = item.get("model")
            if not model:
                continue

            for sub in nested.get(model, []):
                sub_model = sub.get("model")
                if sub_model:
                    inline_map[model]["children"].append(f"{sub_model}Inline")

    # ------------------------------------------------------------
    # 重複排除（重要）
    # ------------------------------------------------------------
    for model, inline in inline_map.items():
        unique = []
        for child in inline["children"]:
            if child not in unique:
                unique.append(child)
        inline["children"] = unique

    # ------------------------------------------------------------
    # inline_order の順に Inline を並べる
    # ------------------------------------------------------------
    ordered_inlines = [
        inline_map[m] for m in inline_order if m in inline_map
    ]

    # ------------------------------------------------------------
    # テンプレート読み込み
    # ------------------------------------------------------------
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("admin.py.j2")

    # DeviceAdmin の register は出力しない
    rendered = template.render(
        models=models,        # ★ これがなかったため import が空になっていた
        inlines=ordered_inlines
    )

    Path(output_file).write_text(rendered)
