# src/amcli/utils/fixture_builder.py

import os
from collections import defaultdict
from amcli.utils.random_generators import (
    generate_random_value,
    generate_gateway_from_cidr,
)

DEBUG = os.environ.get("VERBOSE", "0") != "0"


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
        if DEBUG:
            print("[DEBUG] Using testschema load_order:", order)
    else:
        order = list(models.keys())
        if DEBUG:
            print("[DEBUG] Using fallback model order:", order)

    fixtures = []

    # 参照先モデルの PK を保持する（文字列 PK）
    pk_map = defaultdict(list)

    for model in order:
        if model not in models:
            if DEBUG:
                print(f"[DEBUG] Model '{model}' not in models → skip")
            continue

        fields = models[model]

        if DEBUG:
            print(f"\n[DEBUG] === Generating fixtures for model: {model} ===")

        # まず PK を count 個生成して pk_map に登録する
        model_pks = []
        for pk_index in range(1, count + 1):
            # PK フィールド名を特定（例: device_id, os_id）
            pk_field = None
            for fname, fdef in fields.items():
                if fdef.get("primary_key", False):
                    pk_field = fname
                    break

            if pk_field is None:
                raise ValueError(f"Model {model} に primary_key がありません")

            # PK を文字列で生成
            pk_value = generate_random_value(model, pk_field, fields[pk_field], count, pk_index, name_data)
            model_pks.append(pk_value)

        pk_map[model.lower()] = model_pks

        if DEBUG:
            print(f"[DEBUG]   PK map updated for {model}: {pk_map[model.lower()]}")

        # PK を使って fixture を生成
        for pk_index, pk_value in enumerate(model_pks):
            item = {
                "model": f"myapp.{model.lower()}",
                "pk": pk_value,
                "fields": {}
            }

            if DEBUG:
                print(f"[DEBUG]   PK={pk_value}")

            for fname, fdef in fields.items():
                ftype = fdef["type"]

                # primary_key は fields に入れない（Django loaddata の仕様）
                if fdef.get("primary_key", False):
                    continue

                # ForeignKey / OneToOneField
                if ftype in ("ForeignKey", "OneToOneField"):
                    target = fdef["to"].lower()

                    # 参照先の PK を pk_map から取得（文字列 PK）
                    fk_value = pk_map[target][pk_index % len(pk_map[target])]
                    item["fields"][fname] = fk_value

                    if DEBUG:
                        print(f"[DEBUG]     FK field '{fname}' → target '{target}', assigned PK={fk_value}")

                    continue

                # ManyToManyField
                if ftype == "ManyToManyField":
                    target = fdef["to"].lower()

                    # M2M は複数参照できるが、ここでは 1 件だけ割り当てる
                    m2m_value = [pk_map[target][pk_index % len(pk_map[target])]]
                    item["fields"][fname] = m2m_value

                    if DEBUG:
                        print(f"[DEBUG]     M2M field '{fname}' → target '{target}', assigned PK list={m2m_value}")

                    continue

                # 通常フィールドはランダム生成
                value = generate_random_value(model, fname, fdef, count, pk_index + 1, name_data)
                item["fields"][fname] = value

                if DEBUG:
                    print(f"[DEBUG]     Field '{fname}' → {value}")

            # gateway の自動生成
            if "addresses" in item["fields"] and "gateway" in item["fields"]:
                addrs = item["fields"]["addresses"]
                if addrs:
                    gw = generate_gateway_from_cidr(addrs[0])
                    item["fields"]["gateway"] = gw

                    if DEBUG:
                        print(f"[DEBUG]     Auto gateway from {addrs[0]} → {gw}")

            fixtures.append(item)

    if DEBUG:
        print("\n[DEBUG] === Fixture generation complete ===")
        print(f"[DEBUG] Total fixtures: {len(fixtures)}")

    return fixtures
