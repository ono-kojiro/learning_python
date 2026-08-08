from .client import OPNsenseClient


class VirtualIPAPI:
    """
    Virtual IP API wrapper using interfaces/vip_settings.
    """

    BASE = "/api/interfaces/vip_settings"

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def list_virtual_ips(self):
        return self.client.get(f"{self.BASE}/get")

    def search_virtual_ips(self):
        return self.client.post(f"{self.BASE}/search_item", json={"current": 1, "rowCount": 999})

    def add_virtual_ip(self, vip_data: dict):
        return self.client.post(f"{self.BASE}/add_item", json=vip_data)

    def delete_virtual_ip(self, uuid: str):
        return self.client.post(f"{self.BASE}/del_item/{uuid}")

    def update_virtual_ip(self, uuid: str, vip_data: dict):
        return self.client.post(f"{this.BASE}/set_item/{uuid}", json=vip_data)

