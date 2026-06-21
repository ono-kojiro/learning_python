# amcli/commands/generate_admin.py

from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

from amcli.utils.constants import FieldType, normalize_field_type


def read_yaml(filepath):
    with open(filepath, mode="r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# Inline クラス生成（対象モデルの子モデルのみ）
# ---------------------------------------------------------
def generate_inline_blocks(target_model, model_defs, children_map):
    inline_blocks = []
    inline_class_names = []

    for child in children_map.get(target_model, []):
        child_def = model_defs.get(child)
        if not child_def:
            continue

        fields = child_def.get("fields", {})
        inline_model_expr = None
        inline_class_name = None

        # 子モデルのフィールドを調べて親を参照しているものを探す
        for fname, fdef in fields.items():
            if fdef.get("to") != target_model:
                continue

            ftype = normalize_field_type(fdef.get("type"))

            # ForeignKey / OneToOne → Inline
            if ftype in (FieldType.FOREIGN_KEY, FieldType.ONE_TO_ONE):
                inline_model_expr = f"{child}"
                inline_class_name = f"{child}Inline"
                break

            # ManyToMany → through モデルを Inline
            if ftype == FieldType.MANY_TO_MANY:
                inline_model_expr = f"{child}.{fname}.through"
                inline_class_name = f"{child}{fname.capitalize()}Inline"
                break

        if inline_model_expr:
            block = (
                f"from myapp.models.{child.lower()}_model import {child}\n"
                f"class {inline_class_name}(admin.TabularInline):\n"
                f"    model = {inline_model_expr}\n"
                f"    extra = 0\n"
                f"    show_change_link = True\n\n"
            )
            inline_blocks.append(block)
            inline_class_names.append(inline_class_name)

    return inline_blocks, inline_class_names


# ---------------------------------------------------------
# amcli 用 run() 関数
# ---------------------------------------------------------
def run(loader_dir, output_file, schema_yaml, ref_yaml):
    # ref_yaml から対象モデル名を取得
    ref_data = read_yaml(ref_yaml)
    target_model = ref_data["name"]

    # schema.yaml 読み込み
    schema = read_yaml(schema_yaml)
    depend_map = schema["dependencies"]
    model_defs = schema["models"]

    # reverse dependency map
    children_map = {model: [] for model in depend_map}
    for model, deps in depend_map.items():
        for parent in deps:
            children_map[parent].append(model)

    # Jinja2
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    template = env.get_template("admin_template.j2")

    # Inline と Admin クラス生成
    inline_blocks, inline_class_names = generate_inline_blocks(
        target_model, model_defs, children_map
    )

    content = template.render(
        model=target_model,
        inline_blocks=inline_blocks,
        inline_class_names=inline_class_names,
    )

    # 出力
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content)

    print(f"[amcli] Generated admin: {out_path}")
