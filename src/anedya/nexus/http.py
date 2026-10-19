"""HTTP transport — used when the caller explicitly selects HTTP."""

import httpx
from google.protobuf import json_format
from google.protobuf.message import Message as ProtoMessage

from .config import ClientConfig
from .errors import ConnectionError, TransportError


class HttpTransport:
    """Sync HTTP transport using ``httpx``."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._client: httpx.Client | None = None

    def connect(self) -> None:
        if self._client is not None:
            return

        self._client = httpx.Client(
            base_url=self._config.http_base_url,
            headers={
                **self._config.auth_headers,
                "content-type": "application/json",
                "accept": "application/json",
            },
            timeout=self._config.timeout,
        )

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def unary(
        self,
        service: str,
        method: str,
        request: ProtoMessage,
        response_type: type[ProtoMessage],
        timeout: float | None = None,
    ) -> ProtoMessage:
        """Make an HTTP POST call (mirrors the gRPC unary interface)."""
        if self._client is None:
            raise ConnectionError("Not connected. Call connect() first.")

        url = f"/{method}"
        payload = json_format.MessageToDict(request, preserving_proto_field_name=True)

        response = self._client.post(url, json=payload, timeout=timeout or self._config.timeout)

        if response.status_code >= 400:
            raise TransportError(f"HTTP {response.status_code}: {response.text}")

        result = response_type()
        json_format.ParseDict(response.json(), result)
        return result
