import json
from opnsense.core.system.status import sync_detailed
from opnsense.basic_auth_client import BasicAuthClient

def test_core_system_status(api_config):
    base_url, key, secret = api_config

    client = BasicAuthClient(
        base_url=base_url,
        api_key=key,
        api_secret=secret,
        verify_ssl=False,
    )

    r = sync_detailed(client=client)

    # openapi-python-client の Response は .json() を持たない
    data = json.loads(r.content)

    assert "metadata" in data
    assert "system" in data["metadata"]
    assert "status" in data["metadata"]["system"]
    assert data["metadata"]["system"]["status"] in [0, 1, 2]
