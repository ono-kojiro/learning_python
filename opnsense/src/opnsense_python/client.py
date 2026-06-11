import requests
from .exceptions import OPNsenseAPIError, AuthenticationError, NotFoundError


class OPNsenseClient:
    """
    Base client for accessing OPNsense API.
    """

    def __init__(self, base_url: str, key: str, secret: str, verify_ssl: bool = False):
        self.base_url = base_url.rstrip("/")
        self.auth = (key, secret)
        self.verify_ssl = verify_ssl

    def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"

        try:
            response = requests.request(
                method,
                url,
                auth=self.auth,
                verify=self.verify_ssl,
                **kwargs
            )
        except requests.RequestException as e:
            raise OPNsenseAPIError(f"Request failed: {e}")

        if response.status_code == 401:
            raise AuthenticationError("Authentication failed")

        if response.status_code == 404:
            raise NotFoundError(f"Endpoint not found: {path}")

        if not response.ok:
            raise OPNsenseAPIError(
                f"API error {response.status_code}: {response.text}"
            )

        return response.json()

    def get(self, path: str):
        return self._request("GET", path)

    def post(self, path: str, json=None):
        return self._request("POST", path, json=json)


