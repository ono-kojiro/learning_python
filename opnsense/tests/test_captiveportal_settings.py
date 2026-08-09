import json
from opnsense.captiveportal import Captiveportal


def test_captiveportal_searchzones(client):
    api = Captiveportal(client)
    data = api.search_zones()

    # searchzones は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_captiveportal_getzone(client):
    api = Captiveportal(client)
    data = api.get_zone()

    # getzone は zone 情報を返す（空でもOK）
    # OPNsense 26.7 では "zone" または "zones" が返る
    assert any(k in data for k in ["zone", "zones"])

    if "zone" in data:
        assert isinstance(data["zone"], dict)

    if "zones" in data:
        assert isinstance(data["zones"], list)
