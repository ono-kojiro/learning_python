# file: src/opnsense/basic_auth_client.py

import base64
import httpx
from opnsense.client import Client


class BasicAuthClient(Client):
    def __init__(self, *, base_url: str, api_key: str, api_secret: str, **kwargs):
        super().__init__(base_url=base_url, **kwargs)

        # Basic 認証ヘッダを生成
        token = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
        self._headers["Authorization"] = f"Basic {token}"

    def get_httpx_client(self) -> httpx.Client:
        # 親クラスの get_httpx_client を使うが、Authorization ヘッダが既にセットされている
        return super().get_httpx_client()

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        return super().get_async_httpx_client()


