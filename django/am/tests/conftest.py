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


@pytest.fixture(scope="session", autouse=True)
def rebuild_project():
    original_dir = os.getcwd()

    project_root = os.path.abspath(os.path.join(original_dir, ".."))
    os.chdir(project_root)
    
    subprocess.run(["bash", "build.sh", "stop"], check=True)
    subprocess.run(["bash", "build.sh", "mclean"], check=True)
    subprocess.run(["bash", "build.sh", "all"], check=True)
    subprocess.run(["bash", "build.sh", "start"], check=True)
 
    os.chdir(original_dir)

    yield


def wait_for_server(url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            requests.get(url)
            return True
        except Exception:
            time.sleep(0.5)
    raise RuntimeError("Server did not start in time")

@pytest.fixture(scope="session", autouse=True)
def wait_django_server(configs):
    wait_for_server(configs["base_url"])


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

        # ディレクトリが無ければ作成
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')

        return path
    return _save

