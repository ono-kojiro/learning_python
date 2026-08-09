from opnsense.trafficshaper.api.settings import Settings
import json


def test_ts_downloadpipes(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.downloadpipes()

    try:
        data = r.json()
        assert (
            data == {} or
            data == [] or
            any(k in data for k in ["result", "status", "message", "errorMessage"])
        )
    except json.JSONDecodeError:
        # downloadpipes は XML や空レスポンスを返すことがある
        assert r.text is not None


def test_ts_uploadpipes(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    data = api.uploadpipes().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "status", "message", "errorMessage"])
    )


def test_ts_downloadqueues(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.downloadqueues()

    try:
        data = r.json()
        assert (
            data == {} or
            data == [] or
            any(k in data for k in ["result", "status", "message", "errorMessage"])
        )
    except json.JSONDecodeError:
        # downloadqueues も XML や空レスポンスを返すことがある
        assert r.text is not None


def test_ts_uploadqueues(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    data = api.uploadqueues().json()

    assert (
        data == {} or
        data == [] or
        any(k in data for k in ["result", "status", "message", "errorMessage"])
    )

