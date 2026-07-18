#!/usr/bin/env python3
# file: tools/generate_fixture.py

import sys
import json
import yaml
import getopt
import os
import random
import string


def random_id(prefix):
    return prefix + "-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


def random_value(field_name):
    return field_name.upper() + "-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


def write_yaml(path, data):
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False)


def usage():
    print("Usage: generate_fixture.py -o OUTPUT_FILE spec1.json spec2.json ...")
    sys.exit(1)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
    except getopt.GetoptError:
        usage()

    output_file = None
    for opt, val in opts:
        if opt in ("-o", "--output"):
            output_file = val

    if not output_file:
        print("ERROR: -o OUTPUT_FILE is required")
        usage()

    if not args:
        print("ERROR: No spec JSON files provided")
        usage()

    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    testschema_path = os.path.join(ROOT, "work", "schema", "testschema.json")

    with open(testschema_path, "r") as f:
        testschema = json.load(f)

    fixture_order = testschema.get("fixture_order", [])

    # ------------------------------------------------------------
    # Load specs
    # ------------------------------------------------------------
    models = {}
    for spec_path in args:
        with open(spec_path, "r") as f:
            spec = json.load(f)
        model_name = spec["name"].lower()
        models[model_name] = spec["fields"]

    # ------------------------------------------------------------
    # Generate PKs (PK = *_id)
    # ------------------------------------------------------------
    COUNT = 3
    pk_map = {}

    for model in fixture_order:
        if model not in models:
            continue

        fields = models[model]

        # PK は *_id フィールド
        pk_field = None
        for fname in fields.keys():
            if fname.endswith("_id"):
                pk_field = fname
                break

        if pk_field is None:
            raise ValueError(f"No *_id field found for model {model}")

        pk_list = [random_id(pk_field.upper()) for _ in range(COUNT)]
        pk_map[model] = pk_list

    # ------------------------------------------------------------
    # Generate fixtures
    # ------------------------------------------------------------
    fixtures = []

    for model in fixture_order:
        if model not in models:
            continue

        fields = models[model]
        pk_list = pk_map[model]

        pk_field = None
        for fname in fields.keys():
            if fname.endswith("_id"):
                pk_field = fname
                break

        for idx, pk in enumerate(pk_list):
            item = {
                "model": f"myapp.{model}",
                "pk": pk,
                "fields": {}
            }

            for fname, fdef in fields.items():
                ftype = fdef["type"]

                # 除外
                if fname.startswith("_") or fdef.get("_fixture_ignore", False):
                    continue

                # primary_key フィールド
                if fname == pk_field:
                    item["fields"][fname] = pk
                    continue

                # OneToOneRel → 除外
                if ftype == "OneToOneRel":
                    continue

                # ManyToManyRel（逆参照）除外
                if ftype == "ManyToManyRel":
                    continue

                # OneToManyField → []
                if ftype == "OneToManyField":
                    item["fields"][fname] = []
                    continue

                # JSONField → []
                if ftype == "JSONField":
                    item["fields"][fname] = []
                    continue

                # OneToOneField → index 対応
                if ftype == "OneToOneField":
                    target = fdef["to"].lower()
                    fk_value = pk_map[target][idx % len(pk_map[target])]
                    item["fields"][fname] = fk_value
                    continue

                # ForeignKey → fixture_order に従って割り当て
                if ftype == "ForeignKey":
                    target = fdef["to"].lower()
                    fk_value = pk_map[target][idx % len(pk_map[target])]
                    item["fields"][fname] = fk_value
                    continue

                # ManyToManyField → 正方向のみ
                if ftype == "ManyToManyField":
                    target = fdef["to"].lower()
                    fk_value = pk_map[target][idx % len(pk_map[target])]
                    item["fields"][fname] = [fk_value]
                    continue

                # その他（CharField / TextField）
                item["fields"][fname] = random_value(fname)

            fixtures.append(item)

    write_yaml(output_file, fixtures)


if __name__ == "__main__":
    main()
