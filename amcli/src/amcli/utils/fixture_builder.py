# src/amcli/utils/fixture_builder.py

import os
import random
from collections import defaultdict

from amcli.utils.random_generators import (
    generate_random_value,
    generate_gateway_from_cidr,
)
from amcli.utils.debug import debug
from amcli.utils.dependencies import topo_sort

DEBUG = os.environ.get("VERBOSE", "0") != "0"


def find_pk_field(model_l, fields):
    for fname, fdef in fields.items():
        if fdef.get("primary_key", False):
            return fname
    raise ValueError(f"Model {model_l} に primary_key がありません")


def generate_item(model_l, pk_value, pk_index, fields, pk_map, name_data, count):
    item = {
        "model": f"myapp.{model_l}",
        "pk": pk_value,
        "fields": {},
    }

    for fname, fdef in fields.items():
        ftype = fdef["type"]

        # primary_key は fixture に書かない
        if fdef.get("primary_key", False):
            continue

        # OneToOneRel（逆参照）は fixture に書かない
        if ftype == "OneToOneRel":
            continue

        # ForeignKey / OneToOneField
        if ftype in ("ForeignKey", "OneToOneField"):
            target = fdef["to"].lower()

            # OneToOneField は 1対1 対応
            if ftype == "OneToOneField":
                fk_value = pk_map[target][pk_index % len(pk_map[target])]
            else:
                # ForeignKey はランダムでOK
                fk_value = random.choice(pk_map[target])

            item["fields"][fname] = fk_value
            continue

        # ManyToManyField
        if ftype == "ManyToManyField":
            target = fdef["to"].lower()
            m2m_value = [pk_map[target][pk_index % len(pk_map[target])]]
            item["fields"][fname] = m2m_value
            continue

        # 通常フィールド
        value = generate_random_value(
            model_l,
            fname,
            fdef,
            count,
            pk_index + 1,
            name_data,
        )
        item["fields"][fname] = value

    # gateway の自動生成
    if "addresses" in item["fields"] and "gateway" in item["fields"]:
        addrs = item["fields"]["addresses"]
        if addrs:
            gw = generate_gateway_from_cidr(addrs[0])
            item["fields"]["gateway"] = gw

    return item


def build_fixtures(models, dependencies, name_data, count, include_deps, testschema=None):
    """
    最新仕様に対応した fixture 生成:
    - PK は文字列
    - FK / O2O / M2M は文字列 PK を参照
    - JSONField はそのまま
    """

    # ★ 依存関係ベースの正しい順序を使う
    if testschema and "load_order" in testschema:
        order = testschema["load_order"]
        debug("[DEBUG] Using testschema load_order: {0}".format(order))
    else:
        order = topo_sort(dependencies)
        debug("[DEBUG] Using topo_sort(dependencies): {0}".format(order))

    fixtures = []

    # 参照先モデルの PK を保持する（文字列 PK）
    pk_map = defaultdict(list)

    # ★ 依存順で PK を生成
    for model in order:
        model_l = model.lower()

        if model_l not in models:
            debug(f"[DEBUG] Model '{model}' not in models → skip")
            continue

        fields = models[model_l]

        debug(f"\n[DEBUG] === Generating PKs for model: {model} ===")

        pk_field = find_pk_field(model_l, fields)

        model_pks = []
        for pk_index in range(1, count + 1):
            pk_value = generate_random_value(
                model_l,
                pk_field,
                fields[pk_field],
                count,
                pk_index,
                name_data,
            )
            model_pks.append(pk_value)

        pk_map[model_l] = model_pks
        debug(f"[DEBUG] pk_map[{model_l}] = {pk_map[model_l]}")

    # ★ 依存順で fixture を生成
    for model in order:
        model_l = model.lower()

        if model_l not in models:
            continue

        fields = models[model_l]
        model_pks = pk_map[model_l]

        debug(f"\n[DEBUG] === Generating fixtures for model: {model} ===")

        for pk_index, pk_value in enumerate(model_pks):
            item = generate_item(
                model_l=model_l,
                pk_value=pk_value,
                pk_index=pk_index,
                fields=fields,
                pk_map=pk_map,
                name_data=name_data,
                count=count,
            )
            fixtures.append(item)

    debug("\n[DEBUG] === Fixture generation complete ===")
    debug(f"[DEBUG] Total fixtures: {len(fixtures)}")

    return fixtures
