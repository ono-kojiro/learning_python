import json
from opnsense.auth import Auth

def test_auth_user_search(client):
    api = Auth(client)
    data = api.search_user()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_auth_user_get(client):
    api = Auth(client)
    data = api.get_user()

    assert "user" in data
    assert isinstance(data["user"], dict)


def test_auth_user_searchapikey(client):
    api = Auth(client)
    # searchapikey は search_user と同じ search.py に入る
    data = api.search_user()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_auth_user_newotpseed(client):
    api = Auth(client)
    data = api.newotpseed_user()

    assert "seed" in data
    assert isinstance(data["seed"], str)
