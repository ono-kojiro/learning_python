from .client import OPNsenseClient


class FirewallAPI:
    """
    Firewall Filter API wrapper.
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def list_rules(self):
        """
        Get all firewall filter rules.
        """
        return self.client.get("/api/firewall/filter/get")

    def add_rule(self, rule_data: dict):
        """
        Add a new firewall rule.
        """
        return self.client.post("/api/firewall/filter/addRule", json=rule_data)

    def delete_rule(self, uuid: str):
        """
        Delete a firewall rule by UUID.
        """
        return self.client.post(f"/api/firewall/filter/delRule/{uuid}")

    def toggle_rule(self, uuid: str):
        """
        Enable/disable a firewall rule.
        """
        return self.client.post(f"/api/firewall/filter/toggleRule/{uuid}")


