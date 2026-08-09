#!/usr/bin/env python3
import os
import shutil

SRC_ROOT = "src/opnsense"
OUT_ROOT = "out/opnsense_client/api"

def relocate():
    for root, dirs, files in os.walk(OUT_ROOT):
        for file in files:
            if not file.endswith(".py"):
                continue

            full_path = os.path.join(root, file)

            # 例: root = out/opnsense_client/api/interfaces_bridgesettings
            rel = os.path.relpath(root, OUT_ROOT)  # interfaces_bridgesettings

            # アンダースコアをスラッシュに変換
            parts = rel.split("_")  # ["interfaces", "bridgesettings"]
            new_dir = os.path.join(SRC_ROOT, *parts)

            os.makedirs(new_dir, exist_ok=True)

            new_path = os.path.join(new_dir, file)

            print(f"Move: {full_path} -> {new_path}")
            shutil.copy2(full_path, new_path)

if __name__ == "__main__":
    relocate()

