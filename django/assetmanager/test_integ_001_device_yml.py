import requests
import urllib3

import yaml
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://192.168.1.72:8000"

CA_CERT = "/home/kojiro/devel/learning_python/django/assetmanager/myrootca.crt"

def test_import_devices_from_yaml():

    ymlpath = Path(__file__).parent / "data" / "devices.yml"
    with open(ymlpath, mode='r', encoding='utf-8') as fp :
        data = yaml.safe_load(fp)
    exps = data['devices']

    url = BASE_URL + "/api/devices/"

    for dev in exps:

        # POST で Device を作成
        r = requests.post(url, json=dev, verify=CA_CERT)
        assert r.status_code == 201

    # GET で作成されたことを確認
    r2 = requests.get(url, verify=CA_CERT)
    assert r2.status_code == 200

    gots = r2.json()
    for dev in exps:
        assert any(d["name"] == dev["name"] for d in gots)


