# amcli/commands/mclean.py

import shutil
from pathlib import Path
import yaml

def load_config():
    with open("config.yml") as f:
        return yaml.safe_load(f)

def run():
    """
    Maintainer clean: remove all generated files under outputdir.
    Equivalent to 'make maintainer-clean'.
    """
    config = load_config()
    outputdir = Path(config["outputdir"])

    if outputdir.exists():
        # ディレクトリ配下をすべて削除（ディレクトリ自体は残す）
        for child in outputdir.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    return outputdir

