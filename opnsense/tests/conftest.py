# tests/conftest.py

import os
import pytest
from dotenv import dotenv_values
import urllib3

from opnsense.basic_auth_client import BasicAuthClient


def pytest_configure(config):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"


@pytest.fixture(autouse=True)
def change_working_directory(monkeypatch, request):
    monkeypatch.chdir(request.fspath.dirname)
    yield


@pytest.fixture(scope="session")
def api_config():
    config = dotenv_values(".env")

    key = config.get("key")
    secret = config.get("secret")
    base_url = config.get("base_url")

    if not base_url:
        raise RuntimeError("ERROR: .env に base_url が設定されていません。")

    return base_url, key, secret


@pytest.fixture(scope="session")
def client(api_config):
    base_url, key, secret = api_config

    return BasicAuthClient(
        base_url=base_url,
        api_key=key,
        api_secret=secret,
        verify_ssl=False,
    )
