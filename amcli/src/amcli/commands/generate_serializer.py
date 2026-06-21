from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

from amcli.utils.constants import FieldType

def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


# ---------------------------------------------------------
# amcli 用 run() 関数
# ---------------------------------------------------------
def run(loader_dir, output_file, schema_yaml, ref_yaml):
    # schema.yaml を読み込む
    schema = read_yaml(schema_yaml)
    dependencies = schema["dependencies"]
    reverse_dependencies = schema["reverse_dependencies"]
    dependency_categories = schema["dependency_categories"]
    nested_map = schema.get("nested", {})   # ★ nested セクション

    # Jinja2 環境
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )

    # ★ これを追加する
    env.globals["FieldType"] = FieldType

    # ref_yaml 読み込み
    data = read_yaml(ref_yaml)
    model = data["name"]
    fields = data["fields"]

    # カテゴリ判定
    dep_cat = dependency_categories.get(model)

    # テンプレート自動選択
    if dep_cat == "m2m_owner":
        template_name = "serializer_m2m_owner.j2"
    elif dep_cat == "m2m_target":
        template_name = "serializer_m2m_target.j2"
    elif dep_cat == "fk_parent":
        template_name = "serializer_fk_parent.j2"
    else:
        template_name = "serializer_normal.j2"

    template = env.get_template(template_name)

    # fields_list の構築（Meta.fields 用）
    fields_list = ["id"] + list(fields.keys())

    # reverse FK を追加（fk_parent の場合のみ）
    rev = reverse_dependencies.get(model, [])
    for other_model in rev:
        fields_list.append(f"{other_model.lower()}s")

    # ★ nested 構造を schema.yaml から取得
    nested_fields = nested_map.get(model, [])

    # テンプレートへ渡す
    content = template.render(
        model=model,
        fields=fields,
        fields_list=fields_list,
        reverse_dependencies=reverse_dependencies,
        nested_fields=nested_fields,
    )

    # 出力
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content + "\n")

    print(f"[amcli] Generated serializer: {out_path}")

