import json
from opnsense.captiveportal.api.settings import Settings

def test_captiveportal_searchzones(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchzones()
    data = r.json()

    # searchzones は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_captiveportal_getzone(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getzone()
    data = r.json()

    # getzone は zone 情報を返す（空でもOK）
    # OPNsense 26.7 では "zone" または "zones" が返る
    assert any(k in data for k in ["zone", "zones"])

    # zone が dict の場合
    if "zone" in data:
        assert isinstance(data["zone"], dict)

    # zones が list の場合
    if "zones" in data:
        assert isinstance(data["zones"], list)

