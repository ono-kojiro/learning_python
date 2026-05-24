# conftest.py

import os
import yaml

import pytest
from pytest import MonkeyPatch

import requests

def pytest_configure(config):
    os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

@pytest.fixture(autouse=True)
def change_working_directory(monkeypatch, request):
    print('INFO: before chdir')
    monkeypatch.chdir(request.fspath.dirname)
    yield
    print('INFO: after chdir')

@pytest.fixture(scope="session")
def configs():
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(tests_dir, "config.yml")
    with open(path) as f:
        return yaml.safe_load(f)

