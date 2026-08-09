import json
from opnsense.auth.user import User

def test_auth_user_search(api_config):
    base_url, key, secret = api_config
    api = User(base_url, api_key=key, api_secret=secret)

    r = api.search()
    data = r.json()

    # search は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_auth_user_get(api_config):
    base_url, key, secret = api_config
    api = User(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    # get は "user" 情報を返す（空でもOK）
    assert "user" in data
    assert isinstance(data["user"], dict)


def test_auth_user_searchapikey(api_config):
    base_url, key, secret = api_config
    api = User(base_url, api_key=key, api_secret=secret)

    r = api.searchapikey()
    data = r.json()

    # searchapikey は "rows" を返す
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_auth_user_newotpseed(api_config):
    base_url, key, secret = api_config
    api = User(base_url, api_key=key, api_secret=secret)

    r = api.newotpseed()
    data = r.json()

    # newotpseed は "seed" を返す
    assert "seed" in data
    assert isinstance(data["seed"], str)

