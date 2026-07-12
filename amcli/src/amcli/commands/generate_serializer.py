import os
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader

from amcli.utils.constants import FieldType

from amcli.utils.debug import debug

DEBUG = os.environ.get("VERBOSE", "0") != "0"

def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def run(loader_dir, output_file, schema_yaml, ref_yaml):
    # schema.yaml 読み込み
    schema = read_yaml(schema_yaml)
    dependencies = schema["dependencies"]
    reverse_dependencies = schema["reverse_dependencies"]
    reverse_dependencies_detail = schema.get("reverse_dependencies_detail", {})
    dependency_categories = schema["dependency_categories"]
    nested_map = schema.get("nested", {})

    # Jinja2 環境
    env = Environment(
        loader=FileSystemLoader(loader_dir),
        autoescape=False
    )
    env.globals["FieldType"] = FieldType

    debug("[DEBUG] loader_dir ={0}".format(loader_dir))
    debug("[DEBUG] templates found: {0}".format(env.list_templates()))

    # specs JSON 読み込み
    data = read_yaml(ref_yaml)
    model = data["name"]
    fields = data["fields"]

    # ---------------------------------------------------------
    # ForeignKey / OneToOne → *_id に変換（write用）
    # ---------------------------------------------------------
    converted_fields = {}
    fk_info = {}   # read/write 両方の情報を保持
    has_fk = False

    for fname, fdef in fields.items():
        ftype = fdef["type"]

        if ftype in [FieldType.FOREIGN_KEY, FieldType.ONE_TO_ONE]:
            has_fk = True

            # write 用 device_id
            converted_fields[f"{fname}_id"] = {
                "type": FieldType.CHAR,
                "required": False,
                "to": fdef["to"],
                "source": fname,  # ★ serializer の source に使う
            }

            # read 用 device
            fk_info[fname] = {
                "to": fdef["to"],
                "type": ftype,
            }

        else:
            converted_fields[fname] = fdef

    # ---------------------------------------------------------
    # ★★★ デバッグプリント：FK 判定とテンプレート選択 ★★★
    # ---------------------------------------------------------
    fk_fields = list(fk_info.keys())
    debug(f"[DEBUG] model = {model}")
    debug(f"[DEBUG] fk fields = {fk_fields}")

    dep_cat = dependency_categories.get(model)

    if dep_cat == "m2m_owner":
        template_name = "serializer_m2m_owner.j2"
    elif dep_cat == "m2m_target":
        template_name = "serializer_m2m_target.j2"
    elif dep_cat == "fk_parent":
        template_name = "serializer_fk_parent.j2"
    else:
        # FK を持つモデルは専用テンプレートへ
        if has_fk:
            template_name = "serializer_normal_fk.j2"
        else:
            template_name = "serializer_normal.j2"

    debug(f"[DEBUG] using template = {template_name}")

    template = env.get_template(template_name)

    # ---------------------------------------------------------
    # fields_list の構築（Meta.fields 用）
    # ---------------------------------------------------------
    fields_list = ["id"]

    for fname, fdef in fields.items():
        if fdef["type"] in [FieldType.FOREIGN_KEY, FieldType.ONE_TO_ONE]:
            # read 用
            fields_list.append(fname)
            # write 用
            fields_list.append(f"{fname}_id")
        else:
            fields_list.append(fname)

    # OneToMany の逆参照フィールド追加
    rev = reverse_dependencies.get(model, [])
    for other_model in rev:
        rel = reverse_dependencies_detail.get(other_model)
        if rel and rel.get("type") == "OneToMany":
            fields_list.append(f"{other_model.lower()}s")

    nested_fields = nested_map.get(model, [])

    # ---------------------------------------------------------
    # テンプレートへ渡す
    # ---------------------------------------------------------
    content = template.render(
        model=model,
        fields=fields,
        converted_fields=converted_fields,
        fk_info=fk_info,  # ★ read/write 両方の情報
        fields_list=fields_list,
        reverse_dependencies=reverse_dependencies,
        reverse_dependencies_detail=reverse_dependencies_detail,
        nested_fields=nested_fields,
    )

    # 出力
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as fp:
        fp.write(content + "\n")

    debug(f"[amcli] Generated serializer: {out_path}")
