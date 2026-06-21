# amcli/commands/configure.py

import os
import yaml
from jinja2 import Environment, FileSystemLoader


def load_config():
    with open("config.yml") as f:
        return yaml.safe_load(f)


def run(output_file, application, project):
    """
    Generate build.ninja from Jinja2 templates.
    This version matches build.ninja-reference exactly,
    but spec_order / specs / spec_jsons は config.yml から取得する。
    """

    # ----------------------------------------
    # config.yml を読み込む
    # ----------------------------------------
    config = load_config()

    # CLI 引数が優先、なければ config.yml の値を使う
    project = project or config["project"]
    application = application or config["application"]

    # outputdir（例: work）
    outputdir = config["outputdir"]

    # ----------------------------------------
    # entities（辞書）から spec_order を生成
    # ※ 順序は辞書のキー順（Python3.7+ は定義順保持）
    # ----------------------------------------
    entities = config["entities"]  # dict: { device: specs/device.yml, ... }

    spec_order = list(entities.keys())  # ["device", "netif", ...]
    specs = [entities[name] for name in spec_order]  # ["specs/device.yml", ...]
    spec_jsons = [f"{outputdir}/specs/{name}.json" for name in spec_order]

    # ----------------------------------------
    # makemigrations の依存リスト（従来通り）
    # ----------------------------------------
    makemigrations_list = []

    # models
    makemigrations_list += [
        f"{outputdir}/{application}/models/{name}_model.py"
        for name in spec_order
    ]

    # admin
    makemigrations_list += [
        f"{outputdir}/{application}/admin/{name}_admin.py"
        for name in spec_order
    ]

    # views
    makemigrations_list += [
        f"{outputdir}/{application}/views/{name}_view.py"
        for name in spec_order
    ]

    # serializers
    makemigrations_list += [
        f"{outputdir}/{application}/serializers/{name}_serializer.py"
        for name in spec_order
    ]

    # その他（従来通り）
    makemigrations_list += [
        f"{outputdir}/{application}/admin/__init__.py",
        f"{outputdir}/{application}/views/__init__.py",
        f"{outputdir}/{application}/urls_api.py",
        f"{outputdir}/{application}/loader.py",
        f"{outputdir}/{application}/apps.py",
        f"{outputdir}/{application}/models/__init__.py",
        f"{outputdir}/.rmdb",
    ]

    # ----------------------------------------
    # loaddata の依存リスト（従来通り）
    # ----------------------------------------
    loaddata_list = [
        f"tests/data/test_{name}-fixtures.yaml"
        for name in spec_order
    ]

    # ----------------------------------------
    # Jinja2 環境設定
    # ----------------------------------------
    env = Environment(
        loader=FileSystemLoader("template/build"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    tmpl = env.get_template("build.ninja.j2")

    # ----------------------------------------
    # テンプレートへ渡すコンテキスト
    # ----------------------------------------
    context = {
        "project": project,
        "app": application,
        "spec_order": spec_order,
        "specs": specs,
        "spec_jsons": spec_jsons,
        "makemigrations_list": makemigrations_list,
        "loaddata_list": loaddata_list,
        "outputdir": outputdir,
    }

    # ----------------------------------------
    # build.ninja を生成
    # ----------------------------------------
    rendered = tmpl.render(**context)

    with open(output_file, "w") as f:
        f.write(rendered + '\n')

    print(f"Generated {output_file}")
