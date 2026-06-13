#!/usr/bin/env python3

import sys
import getopt
import yaml


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def generate_test_for_entity(fp, model, general_category, dependency_category):
    model_lower = model.lower()
    url = f"/api/{model_lower}s/"

    fp.write(f"# Generated test for {model}\n")
    fp.write("import requests\n")
    fp.write("import pytest\n\n")

    fp.write("@pytest.mark.order(1)\n")
    fp.write(f"def test_{model_lower}_basic_crud(configs):\n")
    fp.write(f"    base = configs['base_url'] + '{url}'\n\n")

    # ------------------------------------------------------------
    # no_dependency / fk_child → 単純 CRUD
    # ------------------------------------------------------------
    if dependency_category in ("no_dependency", "fk_child"):
        fp.write("    # Create\n")
        fp.write("    item = {}\n")
        fp.write("    res = requests.post(base, json=item)\n")
        fp.write("    assert res.status_code == 201\n\n")

        fp.write("    # List\n")
        fp.write("    res = requests.get(base)\n")
        fp.write("    assert res.status_code == 200\n\n")

        fp.write("    # Delete\n")
        fp.write("    obj_id = res.json()[0]['id']\n")
        fp.write("    res = requests.delete(base + f\"{obj_id}/\")\n")
        fp.write("    assert res.status_code == 204\n\n")
        return

    # ------------------------------------------------------------
    # fk_parent → reverse GET テスト
    # ------------------------------------------------------------
    if dependency_category == "fk_parent":
        fp.write("    # Create parent\n")
        fp.write("    parent = {}\n")
        fp.write("    res = requests.post(base, json=parent)\n")
        fp.write("    assert res.status_code == 201\n")
        fp.write("    pid = res.json()['id']\n\n")

        fp.write("    # GET reverse children\n")
        fp.write("    res = requests.get(base + f\"{pid}/\")\n")
        fp.write("    assert res.status_code == 200\n")
        fp.write("    assert 'ipv4s' in res.json() or 'devices' in res.json()\n\n")
        return

    # ------------------------------------------------------------
    # m2m_owner → PATCH で M2M 更新
    # ------------------------------------------------------------
    if dependency_category == "m2m_owner":
        fp.write("    # Create owner\n")
        fp.write("    owner = {}\n")
        fp.write("    res = requests.post(base, json=owner)\n")
        fp.write("    assert res.status_code == 201\n")
        fp.write("    oid = res.json()['id']\n\n")

        fp.write("    # PATCH M2M\n")
        fp.write("    patch = { 'device_ids': [] }\n")
        fp.write("    res = requests.patch(base + f\"{oid}/\", json=patch)\n")
        fp.write("    assert res.status_code == 200\n\n")
        return

    # ------------------------------------------------------------
    # m2m_target → reverse M2M GET
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # m2m_target → reverse M2M GET
    # ------------------------------------------------------------
    if dependency_category == "m2m_target":
        fp.write("    # Create target with required fields\n")
        fp.write("    target = {\n")
        fp.write("        'device_id': 'DEV-TEST',\n")
        fp.write("        'name': 'Device Test',\n")
        fp.write("        'serial_number': 'SN-TEST'\n")
        fp.write("    }\n")
        fp.write("    res = requests.post(base, json=target)\n")
        fp.write("    assert res.status_code == 201\n")
        fp.write("    tid = res.json()['id']\n\n")

        fp.write("    # GET reverse M2M\n")
        fp.write("    res = requests.get(base + f\"{tid}/\")\n")
        fp.write("    assert res.status_code == 200\n")
        fp.write("    assert 'managers' in res.json()\n\n")
        return


def main():
    options, args = getopt.getopt(
        sys.argv[1:], "hvo:c:", ["help", "version", "output=", "category="]
    )

    output = None
    category_yaml = None

    for option, optarg in options:
        if option in ("-o", "--output"):
            output = optarg
        elif option in ("-c", "--category"):
            category_yaml = optarg

    if category_yaml is None:
        print("ERROR: -c category.yaml is required", file=sys.stderr)
        sys.exit(1)

    categories = read_yaml(category_yaml)
    general = categories["general_categories"]
    dependency = categories["dependency_categories"]

    if not args:
        print("ERROR: no model YAML", file=sys.stderr)
        sys.exit(1)

    # 1つの entity だけ生成
    model_yaml = args[0]
    data = read_yaml(model_yaml)
    model = data["name"]

    if output:
        fp = open(output, "w", encoding="utf-8")
    else:
        fp = sys.stdout

    generate_test_for_entity(
        fp,
        model,
        general.get(model),
        dependency.get(model),
    )

    if output:
        fp.close()


if __name__ == "__main__":
    main()

