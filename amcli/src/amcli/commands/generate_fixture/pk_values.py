# src/amcli/commands/generate_fixture/pk_values.py

from amcli.utils.random_generators import generate_random_value

def generate_pk_values(model, pk_field, fields, count, name_data):
    values = []
    for pk_index in range(1, count + 1):
        pk_value = generate_random_value(
            model, pk_field, fields[pk_field], count, pk_index, name_data
        )
        values.append(pk_value)
    return values

