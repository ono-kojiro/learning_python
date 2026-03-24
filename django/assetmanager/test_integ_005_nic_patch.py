import requests
import urllib3

import yaml
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://192.168.1.72:8000"

CA_CERT = "/home/kojiro/devel/learning_python/django/assetmanager/myrootca.crt"

def test_patch_device_and_nic():

    ymlpath = Path(__file__).parent / "data" / "links.yml"
    with open(ymlpath, mode='r', encoding='utf-8') as fp :
        data = yaml.safe_load(fp)
    links = data['links']


    for link in links:
        nic_id = link['nic_id']
        device_id = link['device_id']

        payload = {
            "device_id": device_id,
        }

        url = BASE_URL + f"/api/nics/{nic_id}/"
        r = requests.patch(
                url,
                json=payload,
                verify=CA_CERT
        )
        assert r.status_code == 200


