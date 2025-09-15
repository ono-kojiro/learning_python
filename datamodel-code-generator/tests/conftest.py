# conftest.py

import pytest
from pytest import MonkeyPatch

@pytest.fixture(autouse=True)
def change_working_directory(monkeypatch, request):
    monkeypatch.chdir(request.fspath.dirname)
    yield



