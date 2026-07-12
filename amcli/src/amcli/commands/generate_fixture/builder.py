# src/amcli/commands/generate_fixture/builder.py

import os
import yaml

from collections import defaultdict

from amcli.utils.random_generators import (
    generate_random_value,
    generate_gateway_from_cidr,
)
from amcli.utils.debug import debug

DEBUG = os.environ.get("VERBOSE", "0") != "0"


def find_pk_field(model, fields):
    """
    PK フィールドを特定する（最低限の修正）
    - primary_key=True を最優先
    - unique=True も PK とみなす（cmp2ref の新仕様）
    """
    # primary_key があれば最優先
    for fname, fdef in fields.items():
        if fdef.get("primary_key", False):
            return fname

    # unique=True のフィールドも PK とみなす
    for fname, fdef in fields.items():
        if fdef.get("unique", False):
            return fname

    raise ValueError(f"Model {model} に primary_key がありません")


def generate_pk_values(model, pk_field, fields, count, name_data):
    """
    PK の値を count 個生成する
    """
    values = []
    for pk_index in range(1, count + 1):
        pk_value = generate_random_value(
            model,
            pk_field,
            fields[pk_field],
            count,
            pk_index,
            name_data,
        )
        values.append(pk_value)
    return values


def assign_field_value(model, fname, fdef, pk_index, pk_map, name_data, count):
    """
    各フィールドの値を生成する（FK / M2M / 通常フィールド）
    """
    ftype = fdef["type"]

    # ForeignKey / OneToOneField
    if ftype in ("ForeignKey", "OneToOneField"):
        target = fdef["to"].lower()
        return pk_map[target][pk_index % len(pk_map[target])]

    # ManyToManyField
    if ftype == "ManyToManyField":
        target = fdef["to"].lower()
        return [pk_map[target][pk_index % len(pk_map[target])]]

    # 通常フィールド
    return generate_random_value(
        model,
        fname,
        fdef,
        count,
        pk_index + 1,
        name_data,
    )


def build_fixtures(models, dependencies, name_data, count, include_deps, testschema=None):
    """
    最新仕様に対応した fixture 生成:
    - PK は文字列（device_id, os_id, manager_id など）
    - FK / O2O / M2M は文字列 PK を参照
    - JSONField はそのまま
    """

    # load_order を使う（最優先）
    if testschema and "load_order" in testschema:
        order = testschema["load_order"]
        debug("[DEBUG] Using testschema load_order: {0}".format(order))
    else:
        order = list(models.keys())
        debug("[DEBUG] Using fallback model order: {0}".format(order))

    fixtures = []

    # 参照先モデルの PK を保持する（文字列 PK）
    pk_map = defaultdict(list)

    for model in order:
        if model not in models:
            debug(f"[DEBUG] Model '{model}' not in models → skip")
            continue

        fields = models[model]

        debug(f"\n[DEBUG] === Generating fixtures for model: {model} ===")

        # PK フィールドの特定（最低限修正済み）
        pk_field = find_pk_field(model, fields)

        # PK を count 個生成して pk_map に登録する
        model_pks = generate_pk_values(model, pk_field, fields, count, name_data)
        pk_map[model.lower()] = model_pks

        debug(f"[DEBUG]   PK map updated for {model}: {pk_map[model.lower()]}")

        # PK を使って fixture を生成
        for pk_index, pk_value in enumerate(model_pks):
            item = {
                "model": f"myapp.{model.lower()}",
                "pk": pk_value,
                "fields": {},
            }

            debug(f"[DEBUG]   PK={pk_value}")

            for fname, fdef in fields.items():
                # primary_key は fields に入れない（Django loaddata の仕様）
                if fdef.get("primary_key", False):
                    continue

                value = assign_field_value(
                    model,
                    fname,
                    fdef,
                    pk_index,
                    pk_map,
                    name_data,
                    count,
                )
                item["fields"][fname] = value

                debug(f"[DEBUG]     Field '{fname}' → {value}")

            # gateway の自動生成
            if "addresses" in item["fields"] and "gateway" in item["fields"]:
                addrs = item["fields"]["addresses"]
                if addrs:
                    gw = generate_gateway_from_cidr(addrs[0])
                    item["fields"]["gateway"] = gw

                    debug(f"[DEBUG]     Auto gateway from {addrs[0]} → {gw}")

            fixtures.append(item)

    debug("\n[DEBUG] === Fixture generation complete ===")
    debug(f"[DEBUG] Total fixtures: {len(fixtures)}")

    return fixtures


def run(loader_dir, output_file, schema_yaml, testschema_yaml, names_yaml, ref_yaml_list,
        count=10, include_deps=False):
    """
    generate_fixture.py の run() を builder.py に移行したもの。
    CLI の引数順と完全一致させている。
    """

    # --- schema.yaml ---
    with open(schema_yaml, "r", encoding="utf-8") as fp:
        models = yaml.safe_load(fp)

    # --- testschema.yaml ---
    with open(testschema_yaml, "r", encoding="utf-8") as fp:
        testschema = yaml.safe_load(fp)

    # --- names.yaml ---
    with open(names_yaml, "r", encoding="utf-8") as fp:
        name_data = yaml.safe_load(fp)

    # --- ref yaml list ---
    dependencies = []
    for ref in ref_yaml_list:
        # ref がディレクトリならスキップ（"." が混入するケースへの対策）
        if os.path.isdir(ref):
            continue
        with open(ref, "r", encoding="utf-8") as fp:
            dependencies.append(yaml.safe_load(fp))

    # --- fixture 生成 ---
    fixtures = build_fixtures(
        models=models,
        dependencies=dependencies,
        name_data=name_data,
        count=count,
        include_deps=include_deps,
        testschema=testschema,
    )

    # --- YAML 出力 ---
    with open(output_file, "w", encoding="utf-8") as fp:
        yaml.safe_dump(fixtures, fp, allow_unicode=True)

    print(f"[amcli] Generated fixture: {output_file}")

