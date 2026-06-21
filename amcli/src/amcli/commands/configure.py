# amcli/commands/configure.py

import os
from jinja2 import Environment, FileSystemLoader


def run(output_file, application, project):
    """
    Generate build.ninja from Jinja2 templates.
    This version matches build.ninja-reference exactly.
    """

    # ----------------------------------------
    # 固定 spec 順序（reference と完全一致）
    # ----------------------------------------
    spec_order = [
        "device",
        "netif",
        "ipv4",
        "comment",
        "manager",
        "remark",
        "os",
    ]

    specs = [f"specs/{name}.yml" for name in spec_order]
    spec_jsons = [f"work/specs/{name}.json" for name in spec_order]

    # ----------------------------------------
    # makemigrations の依存リスト（1 行で出力するために Python 側で構築）
    # ----------------------------------------
    makemigrations_list = []

    # models
    makemigrations_list += [
        f"work/{application}/models/{name}_model.py"
        for name in spec_order
    ]

    # admin
    makemigrations_list += [
        f"work/{application}/admin/{name}_admin.py"
        for name in spec_order
    ]

    # views
    makemigrations_list += [
        f"work/{application}/views/{name}_view.py"
        for name in spec_order
    ]

    # serializers
    makemigrations_list += [
        f"work/{application}/serializers/{name}_serializer.py"
        for name in spec_order
    ]

    # その他
    makemigrations_list += [
        f"work/{application}/admin/__init__.py",
        f"work/{application}/views/__init__.py",
        f"work/{application}/urls_api.py",
        f"work/{application}/loader.py",
        f"work/{application}/apps.py",
        f"work/{application}/models/__init__.py",
        "work/.rmdb",
    ]

    # ----------------------------------------
    # loaddata の依存リスト（1 行で出力）
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
    }

    # ----------------------------------------
    # build.ninja を生成
    # ----------------------------------------
    rendered = tmpl.render(**context)

    with open(output_file, "w") as f:
        f.write(rendered + '\n')

    print(f"Generated {output_file}")
