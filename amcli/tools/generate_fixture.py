#!/usr/bin/env python3
# file: tools/generate_fixture.py

import sys
import json
import yaml
import getopt
import os
import random
import string


def debug(msg):
    print(f"[DEBUG] {msg}")


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

    debug(f"Loading testschema.json from {testschema_path}")

    with open(testschema_path, "r") as f:
        testschema = json.load(f)

    fixture_order = testschema.get("fixture_order", [])
    debug(f"Fixture order: {fixture_order}")

    # ------------------------------------------------------------
    # Load specs
    # ------------------------------------------------------------
    models = {}
    for spec_path in args:
        debug(f"Loading spec: {spec_path}")
        with open(spec_path, "r") as f:
            spec = json.load(f)
        model_name = spec["name"].lower()
        models[model_name] = spec["fields"]
        debug(f"Loaded model '{model_name}' with fields: {list(spec['fields'].keys())}")

    # ------------------------------------------------------------
    # Generate PKs
    # ------------------------------------------------------------
    COUNT = 3
    pk_map = {}

    for model in fixture_order:
        if model not in models:
            debug(f"Model '{model}' not in specs, skipping PK generation")
            continue

        pk_list = [random_id(model.upper()) for _ in range(COUNT)]
        pk_map[model] = pk_list
        debug(f"Generated PKs for {model}: {pk_list}")

    # ------------------------------------------------------------
    # Generate fixtures
    # ------------------------------------------------------------
    fixtures = []

    for model in fixture_order:
        if model not in models:
            debug(f"Model '{model}' not in specs, skipping fixture generation")
            continue

        fields = models[model]
        pk_list = pk_map[model]

        debug(f"Generating fixtures for model '{model}'")

        for idx, pk in enumerate(pk_list):
            debug(f"  Creating item for PK={pk}")

            item = {
                "model": f"myapp.{model}",
                "pk": pk,
                "fields": {}
            }

            for fname, fdef in fields.items():
                ftype = fdef["type"]
                debug(f"    Field '{fname}' type={ftype}")

                # ------------------------------------------------------------
                # ★ アンダースコア除外ロジック
                # ------------------------------------------------------------
                if fname.startswith("_") or fdef.get("_fixture_ignore", False):
                    debug(f"      Skipping field '{fname}' due to underscore-ignore")
                    continue

                # primary_key
                if fdef.get("primary_key", False):
                    debug(f"      Skipping primary_key field '{fname}'")
                    continue

                # OneToOneRel
                if ftype == "OneToOneRel":
                    debug(f"      Skipping OneToOneRel field '{fname}'")
                    continue

                # OS.device（子側 OneToOne）
                if model == "os" and fname == "device":
                    debug(f"      Skipping child OneToOneField '{fname}' in OS")
                    continue

                # ManyToManyRel（逆参照）
                if ftype == "ManyToManyRel":
                    debug(f"      Skipping ManyToManyRel field '{fname}'")
                    continue

                # OneToManyField → []
                if ftype == "OneToManyField":
                    debug(f"      Setting OneToManyField '{fname}' = []")
                    item["fields"][fname] = []
                    continue

                # JSONField → []
                if ftype == "JSONField":
                    debug(f"      Setting JSONField '{fname}' = []")
                    item["fields"][fname] = []
                    continue

                # OneToOneField → 1対1対応
                if ftype == "OneToOneField":
                    target = fdef["to"].lower()
                    fk_value = pk_map[target][idx]
                    debug(f"      OneToOneField '{fname}' → {fk_value}")
                    item["fields"][fname] = fk_value
                    continue

                # ForeignKey → ランダム
                if ftype == "ForeignKey":
                    target = fdef["to"].lower()
                    fk_value = random.choice(pk_map[target])
                    debug(f"      ForeignKey '{fname}' → {fk_value}")
                    item["fields"][fname] = fk_value
                    continue

                # ManyToManyField → 正方向のみ
                if ftype == "ManyToManyField":
                    target = fdef["to"].lower()
                    fk_value = random.choice(pk_map[target])
                    debug(f"      ManyToManyField '{fname}' → [{fk_value}]")
                    item["fields"][fname] = [fk_value]
                    continue

                # その他（CharField / TextField）
                value = random_value(fname)
                debug(f"      Default field '{fname}' → {value}")
                item["fields"][fname] = value

            fixtures.append(item)
            debug(f"  Added fixture item for PK={pk}")

    debug(f"Writing output YAML to {output_file}")
    write_yaml(output_file, fixtures)
    debug("Done.")


if __name__ == "__main__":
    main()
