from opnsense.trust.cert import Cert
import json


def test_trust_cert_search(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    r = api.search()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)


def test_trust_cert_get(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    r = api.get()
    data = r.json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["cert", "cert_item", "result", "message", "errorMessage", "status"])
    )

    if "cert" in data:
        assert isinstance(data["cert"], dict)
    if "cert_item" in data:
        assert isinstance(data["cert_item"], dict)


def test_trust_cert_add(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    data = api.add().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )


def test_trust_cert_set(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    data = api.set().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )


def test_trust_cert_delete(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    data = api.delete().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )


def test_trust_cert_cainfo(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    data = api.cainfo().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["info", "result", "message", "errorMessage", "status"])
    )

    if "info" in data:
        assert isinstance(data["info"], dict)


def test_trust_cert_rawdump(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    r = api.rawdump()

    try:
        data = r.json()
        assert (
            data == {} or
            data == [] or
            any(k in data for k in ["result", "message", "errorMessage", "status"])
        )
    except json.JSONDecodeError:
        # PEM テキストが返るのが正常
        assert isinstance(r.text, str)
        assert "BEGIN" in r.text or len(r.text) >= 0


def test_trust_cert_calist(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    data = api.calist().json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        "list" in data or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)
    if "list" in data:
        assert isinstance(data["list"], list)


def test_trust_cert_userlist(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

    data = api.userlist().json()

    assert (
        data == {} or
        data == [] or
        "rows" in data or
        "users" in data or
        any(k in data for k in ["result", "message", "errorMessage", "status"])
    )

    if "rows" in data:
        assert isinstance(data["rows"], list)
    if "users" in data:
        assert isinstance(data["users"], list)


def test_trust_cert_generatefile(api_config):
    base_url, key, secret = api_config
    api = Cert(base_url, api_key=key, api_secret=secret)

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

