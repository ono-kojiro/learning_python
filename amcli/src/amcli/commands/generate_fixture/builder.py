# file: src/amcli/commands/generate_fixture/builder.py

import os
import random

from collections import defaultdict
from amcli.utils.random_generators import generate_random_value, generate_gateway_from_cidr
from amcli.utils.debug import debug
from .pk import find_pk_field

DEBUG = os.environ.get("VERBOSE", "0") != "0"


# ------------------------------------------------------------
# 1. fixture_order の決定
# ------------------------------------------------------------
def resolve_order(models, testschema):
    if testschema and "fixture_order" in testschema:
        order = testschema["fixture_order"]
        debug("[DEBUG] Using testschema fixture_order: {0}".format(order))
        return order

    order = list(models.keys())
    debug("[DEBUG] Using fallback model order: {0}".format(order))
    return order


# ------------------------------------------------------------
# 2. PK の生成と pk_map の構築
# ------------------------------------------------------------
def generate_pk_map(order, models, name_data, count):
    pk_map = defaultdict(list)

    for model in order:
        model_l = model.lower()
        if model_l not in models:
            debug(f"[DEBUG] SKIP: model_l='{model_l}' not in models keys {list(models.keys())}")
            continue

        fields = models[model_l]
        pk_field = find_pk_field(model_l, fields)
        debug(f"[DEBUG] PK field for model '{model_l}' = {pk_field}")

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

    return pk_map


# ------------------------------------------------------------
# 3. 1 モデルの 1 PK に対する fixture item を生成
# ------------------------------------------------------------
def generate_item(model_l, pk_value, pk_index, fields, pk_map, name_data, count):
    item = {
        "model": f"myapp.{model_l}",
        "pk": pk_value,
        "fields": {},
    }

    for fname, fdef in fields.items():
        ftype = fdef["type"]

        # ★ primary_key は fixture に書かない
        if fdef.get("primary_key", False):
            continue

        # ★ OneToOneRel（逆参照）は fixture に書かない
        if ftype == "OneToOneRel":
            continue

        # ForeignKey / OneToOneField（親側のみ）
        if ftype in ("ForeignKey", "OneToOneField"):

            # OS.device は子側なので除外
            if model_l == "os" and fname == "device":
                continue

            target = fdef["to"].lower()

            # ★ OneToOneField は 1対1 対応にする
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

        # その他のフィールド
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


# ------------------------------------------------------------
# 4. build_fixtures（メイン関数）
# ------------------------------------------------------------
def build_fixtures(models, dependencies, name_data, count, include_deps, testschema=None):

    order = resolve_order(models, testschema)

    debug(f"[DEBUG] models keys at start of build_fixtures: {list(models.keys())}")
    debug(f"[DEBUG] fixture_order: {order}")

    pk_map = generate_pk_map(order, models, name_data, count)

    fixtures = []

    for model in order:
        model_l = model.lower()
        if model_l not in models:
            continue

        fields = models[model_l]
        model_pks = pk_map[model_l]

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
