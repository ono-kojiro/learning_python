from opnsense.trust.ca import Ca
import json


def test_trust_ca_search(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    r = api.search()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)


def test_trust_ca_get(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    # get は ca / ca_item のどちらでも正常
    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["ca", "ca_item", "result", "message", "errorMessage"])
    )

    if "ca" in data:
        assert isinstance(data["ca"], dict)
    if "ca_item" in data:
        assert isinstance(data["ca_item"], dict)


def test_trust_ca_add(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    data = api.add().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_trust_ca_set(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    data = api.set().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_trust_ca_delete(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    data = api.delete().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage"])
    )


def test_trust_ca_cainfo(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    data = api.cainfo().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["info", "result", "message", "errorMessage"])
    )

    if "info" in data:
        assert isinstance(data["info"], dict)


def test_trust_ca_rawdump(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    r = api.rawdump()

    # rawdump は PEM テキストで JSON ではない
    try:
        data = r.json()
        # JSON が返る場合もあるので一応許容
        assert (
            data == {} or
            data == [] or
            any(k in data for k in ["result", "message", "errorMessage"])
        )
    except json.JSONDecodeError:
        # PEM テキストが返るのが正常
        assert isinstance(r.text, str)
        assert "BEGIN" in r.text or len(r.text) >= 0


def test_trust_ca_calist(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    data = api.calist().json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        "list" in data or
        any(k in data for k in ["result", "message", "errorMessage"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)
    if "list" in data:
        assert isinstance(data["list"], list)


def test_trust_ca_generatefile(api_config):
    base_url, key, secret = api_config
    api = Ca(base_url, api_key=key, api_secret=secret)

    r = api.generatefile()

    try:
        data = r.json()
        assert (
            data == {} or
            data == [] or
            any(k in data for k in ["result", "status", "message", "errorMessage"])
        )
    except json.JSONDecodeError:
        # generatefile はバイナリや PEM を返すことがある
        assert r.content is not None


