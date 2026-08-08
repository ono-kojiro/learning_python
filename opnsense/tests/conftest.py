# tests/conftest.py

import os
import pytest
from dotenv import dotenv_values

import urllib3

def pytest_configure(config):
    # 自己署名証明書の警告を抑制
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Requests の CA バンドル設定（必要なら）
    os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

@pytest.fixture(autouse=True)
def change_working_directory(monkeypatch, request):
    """
    以前のテスト環境と互換性を保つために残す。
    テストファイルのディレクトリをカレントにする。
    """
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
