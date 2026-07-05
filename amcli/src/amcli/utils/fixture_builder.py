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
    CRUD と同じアルゴリズムで fixture を生成する。
    testschema.json の load_order を使って依存関係順に生成する。
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

    # 参照先モデルの PK を保持する
    pk_map = defaultdict(list)

    for model in order:
        if model not in models:
            if DEBUG:
                print(f"[DEBUG] Model '{model}' not in models → skip")
            continue

        fields = models[model]

        if DEBUG:
            print(f"\n[DEBUG] === Generating fixtures for model: {model} ===")

        for pk in range(1, count + 1):
            item = {
                "model": f"myapp.{model.lower()}",
                "pk": pk,
                "fields": {}
            }

            if DEBUG:
                print(f"[DEBUG]   PK={pk}")

            for fname, fdef in fields.items():
                ftype = fdef["type"]

                # ForeignKey / OneToOneField
                if ftype in ("ForeignKey", "OneToOneField"):
                    target = fdef["to"].lower()

                    # CRUD と同じ：参照先の PK をそのまま使う
                    fk_value = pk
                    item["fields"][fname] = fk_value

                    if DEBUG:
                        print(f"[DEBUG]     FK field '{fname}' → target '{target}', assigned PK={fk_value}")

                    continue

                # ManyToManyField
                if ftype == "ManyToManyField":
                    target = fdef["to"].lower()
                    item["fields"][fname] = [pk]

                    if DEBUG:
                        print(f"[DEBUG]     M2M field '{fname}' → target '{target}', assigned PK=[{pk}]")

                    continue

                # 通常フィールドはランダム生成
                value = generate_random_value(model, fname, fdef, count, pk, name_data)
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

        # このモデルの PK を保存（FK 割り当てに使う）
        pk_map[model.lower()] = list(range(1, count + 1))

        if DEBUG:
            print(f"[DEBUG]   PK map updated for {model}: {pk_map[model.lower()]}")

    if DEBUG:
        print("\n[DEBUG] === Fixture generation complete ===")
        print(f"[DEBUG] Total fixtures: {len(fixtures)}")

    return fixtures
