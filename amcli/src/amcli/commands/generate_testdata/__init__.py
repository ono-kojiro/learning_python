# src/amcli/commands/generate_testdata/__init__.py

"""
gentestdata command package for amcli.

This package provides the `run` function used by the CLI entrypoint
to generate API testdata JSON files.
"""

from .main import run

__all__ = ["run"]

