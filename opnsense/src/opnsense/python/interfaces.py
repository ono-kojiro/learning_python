from .client import OPNsenseClient


class InterfacesAPI:
    """
    OPNsense Interfaces Overview API (tables format)
    """

    def __init__(self, client: OPNsenseClient):
        self.client = client

    def list_interfaces(self):
        """
        GET /api/interfaces/overview/interfaces_info

        返却例:
        {
          "current": 1,
          "rowCount": 11,
          "rows": [
            { "config": { "identifier": "opt4", ... } },
            ...
          ],
          "total": 11
        }
        """
        return self.client.get("/api/interfaces/overview/interfaces_info")

    def get_interface_keys(self):
        """
        opt1, opt2, lan, wan ... の一覧を返す
        """
        data = self.list_interfaces()

        if "rows" not in data:
            raise RuntimeError(f"Unexpected interface structure: {data}")

        keys = []
        for row in data["rows"]:
            cfg = row.get("config", {})
            ident = cfg.get("identifier")
            if ident:
                keys.append(ident)

        return keys

