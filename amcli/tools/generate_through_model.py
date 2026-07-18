#!/usr/bin/env python3
# file: tools/generate_through_model.py

import sys
import json
import getopt
import re


def safe(name):
    return re.sub(r'\W+', '_', name)


HEADER = """from django.db import models
from .device_model import Device
from .manager_model import Manager

"""


def usage():
    print("Usage: generate_through_model.py -o OUTPUT_FILE schema.json")
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

    if not output_file or not args:
        usage()

    schema_path = args[0]

    with open(schema_path, "r") as f:
        schema = json.load(f)

    nested = schema["nested"]

    print("=== DEBUG: nested ===")
    print(json.dumps(nested, indent=2))

    # Device.managers の many_to_many があれば DeviceManager を生成
    generate_device_manager = False

    for item in nested.get("Device", []):
        if item.get("kind") == "many_to_many" and item.get("name") == "managers":
            generate_device_manager = True

    if generate_device_manager:
        print("=== DEBUG: many_to_many detected: Device.managers ===")
        through_def = """
class DeviceManager(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("device", "manager")
"""
    else:
        print("=== DEBUG: no many_to_many(Device.managers) found ===")
        through_def = ""

    with open(output_file, "w") as f:
        f.write(HEADER)
        f.write(through_def)

    print(f"[OK] Generated through model: {output_file}")


if __name__ == "__main__":
    main()
