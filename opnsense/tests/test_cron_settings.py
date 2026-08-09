from opnsense.cron import Cron


def test_cron_searchjobs(client):
    api = Cron(client)
    data = api.search_jobs()

    # searchjobs は "rows" を返す（空でもOK）
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_cron_getjob(client):
    api = Cron(client)
    data = api.get_job()

    # getjob は job 情報を返す（空でもOK）
    # OPNsense 26.7 では "job" または "jobs" が返る
    assert any(k in data for k in ["job", "jobs"])

    if "job" in data:
        assert isinstance(data["job"], dict)

    if "jobs" in data:
        assert isinstance(data["jobs"], list)
