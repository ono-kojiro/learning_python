#!/usr/bin/env python3

import sys
import getopt
import yaml
import json
import os
import random
import string


def read_yaml(path):
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def random_string(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def generate_test_for_model(model, fields):
    """テストコード文字列を返す（ファイルは main で開く）"""
    model_lower = model.lower()

    out = []
    out.append(f"# Auto-generated CRUD test for {model}")
    out.append("import requests")
    out.append("import pytest")
    out.append("import json\n")

    out.append(f"model = '{model}'")
    out.append(f"fields = json.loads('''{json.dumps(fields)}''')\n")

    # POST body generator
    out.append("def _gen_body(model, fields):")
    out.append("    body = {}")
    out.append("    for fname, fdef in fields.items():")
    out.append("        ftype = fdef['type']")
    out.append("        if ftype == 'CharField':")
    out.append("            body[fname] = model.upper() + '-TEST'")
    out.append("            continue")
    out.append("        if ftype == 'JSONField':")
    out.append("            default = fdef.get('default', None)")
    out.append("            if default == 'dict': body[fname] = {}")
    out.append("            elif default == 'list': body[fname] = []")
    out.append("            else: body[fname] = {}")
    out.append("            continue")
    out.append("        # ForeignKey / OneToOneField → 整数 ID を送る（DRF 標準）")
    out.append("        if ftype in ('ForeignKey', 'OneToOneField'):")
    out.append("            body[fname] = 1")

    #out.append("        if ftype in ('ForeignKey', 'OneToOneField'):")
    #out.append("            # Serializer は <field>_id を受け取る")
    #out.append("            body[fname + '_id'] = 1")

    out.append("            continue")
    out.append("        # ManyToManyField → 整数 ID の配列（DRF 標準）")
    out.append("        if ftype == 'ManyToManyField':")
    out.append("            body[fname] = [1]")
    out.append("            continue")
    out.append("        body[fname] = None")
    out.append("    return body\n")

    # CRUD test
    out.append(f"def test_{model_lower}_crud(configs):")
    out.append(f"    base = configs['base_url'] + '/api/{model_lower}s/'\n")

    out.append("    res = requests.get(base)")
    out.append("    assert res.status_code == 200\n")

    out.append("    item = _gen_body(model, fields)")
    out.append("    res = requests.post(base, json=item)")
    out.append("    assert res.status_code == 201")
    out.append("    obj = res.json()")
    out.append("    obj_id = obj['id']\n")

    out.append("    res = requests.get(base + f'{obj_id}/')")
    out.append("    assert res.status_code == 200\n")

    out.append("    patch_body = {}")
    out.append("    for fname, fdef in fields.items():")
    out.append("        if fdef['type'] == 'CharField':")
    out.append("            patch_body[fname] = 'UPDATED'")
    out.append("            break")
    out.append("    res = requests.patch(base + f'{obj_id}/', json=patch_body)")
    out.append("    assert res.status_code in (200, 202)\n")

    out.append("    res = requests.delete(base + f'{obj_id}/')")
    out.append("    assert res.status_code == 204\n")

    return "\n".join(out) + "\n"


def main():
    options, args = getopt.getopt(
        sys.argv[1:], "ho:m:", ["help", "output=", "meta="]
    )

    output_file = None
    meta_path = None

    for opt, val in options:
        if opt in ("-o", "--output"):
            output_file = val
        elif opt in ("-m", "--meta"):
            meta_path = val

    if not meta_path:
        print("ERROR: meta.yaml is required (-m)")
        return

    if not output_file:
        print("ERROR: output file is required (-o)")
        return

    if len(args) != 1:
        print("ERROR: exactly one *_ref.yaml must be specified")
        return

    # meta.yaml 読み込み
    meta = read_yaml(meta_path)
    meta_models = meta["models"]

    # *_ref.yaml 読み込み
    ref_yaml = args[0]
    data = read_yaml(ref_yaml)
    model = data["name"]
    fields = meta_models[model]["fields"]

    # main の中でファイルを開く
    with open(output_file, "w", encoding="utf-8") as fp:
        fp.write(generate_test_for_model(model, fields))

    print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
