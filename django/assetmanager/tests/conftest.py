# conftest.py

import os
import yaml
import subprocess

import json

import pytest
from pytest import MonkeyPatch
import time

import requests

def pytest_configure(config):
    os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

@pytest.fixture(autouse=True)
def change_working_directory(monkeypatch, request):
    monkeypatch.chdir(request.fspath.dirname)
    yield

@pytest.fixture(scope="session")
def configs():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(tests_dir, "config.yml")
    with open(path) as f:
        return yaml.safe_load(f)

@pytest.fixture
def load_json():
    def _load(filename):
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "exp", filename)
        with open(path) as f:
            return json.load(f)
    return _load

@pytest.fixture
def save_json():
    def _save(filename, data):
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "got", filename)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')

        return path
    return _save
