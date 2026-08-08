import json
from opnsense.cron.api.settings import Settings

def test_cron_searchjobs(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.searchjobs()
    data = r.json()

    # searchjobs は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_cron_getjob(api_config):
    base_url, key, secret = api_config
    api = Settings(base_url, api_key=key, api_secret=secret)

    r = api.getjob()
    data = r.json()

    # getjob は job 情報を返す（空でもOK）
    # OPNsense 26.7 では "job" または "jobs" が返る
    assert any(k in data for k in ["job", "jobs"])

    if "job" in data:
        assert isinstance(data["job"], dict)

    if "jobs" in data:
        assert isinstance(data["jobs"], list)

