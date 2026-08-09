import json
from opnsense.core.system import System

def test_core_system_status(api_config):
    base_url, key, secret = api_config
    api = System(base_url, api_key=key, api_secret=secret)

    r = api.status()
    data = r.json()

    assert "metadata" in data
    assert "system" in data["metadata"]
    assert "status" in data["metadata"]["system"]
    assert data["metadata"]["system"]["status"] in [0, 1, 2]
