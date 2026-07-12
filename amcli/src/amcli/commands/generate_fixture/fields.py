# src/amcli/commands/generate_fixture/fields.py

from amcli.utils.random_generators import (
    generate_random_value,
    generate_gateway_from_cidr,
)

def assign_field_value(model, fname, fdef, pk_index, pk_map, name_data, count):
    ftype = fdef["type"]

    # FK / O2O
    if ftype in ("ForeignKey", "OneToOneField"):
        target = fdef["to"].lower()
        return pk_map[target][pk_index % len(pk_map[target])]

    # M2M
    if ftype == "ManyToManyField":
        target = fdef["to"].lower()
        return [pk_map[target][pk_index % len(pk_map[target])]]

    # 通常フィールド
    return generate_random_value(
        model, fname, fdef, count, pk_index + 1, name_data
    )

