# file: tests/test_diagnostics.py

from opnsense.diagnostics.system import System
from opnsense.diagnostics.firewall import Firewall


# -------------------------
# Diagnostics / System
# -------------------------

def test_diagnostics_system_information(client):
    api = System(client)
    data = api.systeminformation()

    assert "name" in data

    if "versions" in data:
        assert isinstance(data["versions"], list)

    if "updates" in data:
        assert isinstance(data["updates"], str)


def test_diagnostics_system_time(client):
    api = System(client)
    data = api.systemtime()

    assert "boottime" in data

    if "uptime" in data:
        assert isinstance(data["uptime"], str)


def test_diagnostics_system_memory(client):
    api = System(client)
    data = api.memory()

    assert "vmstat" in data
    assert "malloc-statistics" in data["vmstat"]
    assert "memory" in data["vmstat"]["malloc-statistics"]

    assert isinstance(data["vmstat"]["malloc-statistics"]["memory"], list)


# -------------------------
# Diagnostics / Firewall (GET 系のみ)
# -------------------------

def test_diagnostics_firewall_log(client):
    api = Firewall(client)
    data = api.log()

    # log は list または dict のどちらもあり得る
    assert isinstance(data, (dict, list))


def test_diagnostics_firewall_logfilters(client):
    api = Firewall(client)
    data = api.logfilters()
    assert isinstance(data, dict)


def test_diagnostics_firewall_listruleids(client):
    api = Firewall(client)
    data = api.listruleids()
    assert isinstance(data, dict)
