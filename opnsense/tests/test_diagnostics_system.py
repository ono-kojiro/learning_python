from opnsense.diagnostics import Diagnostics


def test_diagnostics_system_information(client):
    api = Diagnostics(client)
    data = api.systeminformation_system()

    # systeminformation は "name" を必ず返す
    assert "name" in data

    # "versions" が存在する場合は list であることを確認
    if "versions" in data:
        assert isinstance(data["versions"], list)

    # "updates" が存在する場合は文字列であることを確認
    if "updates" in data:
        assert isinstance(data["updates"], str)


def test_diagnostics_system_time(client):
    api = Diagnostics(client)
    data = api.systemtime_system()

    # boottime は必ず存在する
    assert "boottime" in data

    # uptime が存在する場合は文字列であることを確認
    if "uptime" in data:
        assert isinstance(data["uptime"], str)


def test_diagnostics_system_memory(client):
    api = Diagnostics(client)
    data = api.memory_system()

    # vmstat → malloc-statistics → memory の階層構造
    assert "vmstat" in data
    assert "malloc-statistics" in data["vmstat"]
    assert "memory" in data["vmstat"]["malloc-statistics"]

    # memory は list である
    assert isinstance(data["vmstat"]["malloc-statistics"]["memory"], list)
