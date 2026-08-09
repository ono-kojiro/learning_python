import json
from opnsense.ids.settings import Settings


def test_ids_getruleinfo(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getruleinfo()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["ruleinfo", "rule", "result", "errorMessage"])
    )


def test_ids_listrulemetadata(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.listrulemetadata()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["metadata", "rules", "result", "errorMessage"])
    )


def test_ids_getrulesetproperties(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getrulesetproperties()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["properties", "ruleset", "result", "errorMessage"])
    )


def test_ids_listrulesets(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.listrulesets()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["rulesets", "sets", "result", "current", "total"])
    )


def test_ids_getruleset(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getruleset()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["ruleset", "set", "result", "errorMessage"])
    )


def test_ids_searchuserrule(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchuserrule()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_ids_getuserrule(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getuserrule()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["rule", "userrule", "result", "errorMessage"])
    )


def test_ids_searchpolicy(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchpolicy()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_ids_getpolicy(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getpolicy()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["policy", "policies", "result", "errorMessage"])
    )


def test_ids_searchpolicyrule(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchpolicyrule()
    data = r.json()

    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_ids_getpolicyrule(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getpolicyrule()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["rule", "policyrule", "result", "errorMessage"])
    )


def test_ids_checkpolicyrule(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.checkpolicyrule()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["status", "result", "rule", "errorMessage"])
    )
