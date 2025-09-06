# conftest.py

import pytest
from pytest import MonkeyPatch

@pytest.fixture(autouse=True)
def hoge():
    print('Hoge')

@pytest.fixture(autouse=True)
def change_working_directory(monkeypatch, request):
    print('INFO: before chdir')
    monkeypatch.chdir(request.fspath.dirname)
    yield
    print('INFO: after chdir')



