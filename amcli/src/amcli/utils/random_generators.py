# src/amcli/utils/random_generators.py

import random
import string
import datetime
from amcli.utils.constants import FieldType, normalize_field_type


def random_string(prefix, length=6):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_human_name(name_data):
    first = name_data.get("first_names", [])
    last = name_data.get("last_names", [])
    if not first or not last:
        return "Unknown User"
    return random.choice(first) + " " + random.choice(last)


def generate_random_cidr_ipv4(prefix=24):
    x = random.randint(0, 255)
    y = random.randint(1, 254)
    return f"192.168.{x}.{y}/{prefix}"


def generate_jsonfield_value(field_name, field_def):
    default = field_def.get("default", None)

    if field_name == "addresses":
        count = random.randint(1, 4)
        return [generate_random_cidr_ipv4() for _ in range(count)]

    if field_name == "dns":
        return [f"8.8.8.{random.randint(1, 254)}"]

    if default == "list":
        return []

    if default == "dict":
        return {}

    return []


def generate_gateway_from_cidr(cidr):
    ip, prefix = cidr.split("/")
    a, b, c, d = ip.split(".")
    return f"{a}.{b}.{c}.1"


def random_datetime():
    JST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(JST)
    delta_days = random.randint(0, 3650)
    dt = now - datetime.timedelta(days=delta_days)
    return dt.isoformat()


def random_date():
    now = datetime.date.today()
    delta_days = random.randint(0, 3650)
    d = now - datetime.timedelta(days=delta_days)
    return d.strftime("%Y-%m-%d")


def generate_random_value(model, field_name, field_def, count, pk, name_data):
    ftype = normalize_field_type(field_def["type"])
    null_ok = field_def.get("null", False)

    if model == "Manager" and field_name == "name":
        return random_human_name(name_data)

    if ftype == FieldType.JSON:
        return generate_jsonfield_value(field_name, field_def)

    if field_name == "gateway":
        return None

    if ftype == FieldType.CHAR:
        return random_string(f"{model.upper()}-")

    if ftype.value == "GenericIPAddressField":
        return f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"

    if ftype == FieldType.DATETIME:
        return random_datetime()

    if ftype == FieldType.DATE:
        return random_date()

    if ftype == FieldType.ONE_TO_ONE:
        return pk

    if ftype == FieldType.FOREIGN_KEY:
        if null_ok and random.random() < 0.2:
            return None
        return random.randint(1, count)

    if ftype == FieldType.MANY_TO_MANY:
        n = random.randint(1, min(3, count))
        return random.sample(list(range(1, count + 1)), n)

    if null_ok:
        return None

    return random_string("VAL-")

