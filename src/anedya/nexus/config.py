"""Configuration for the Anedya Nexus SDK."""

import os
from dataclasses import dataclass, field


@dataclass
class ClientConfig:
    """SDK configuration.

    Authentication priority (highest → lowest):
        1. Explicit ``api_key`` passed to the constructor
        2. ``ANEDYA_API_KEY`` environment variable
        3. ``ANEDYA_SERVICE_TOKEN`` environment variable

    Parameters
    ----------
    api_key : str, optional
        Anedya API key.
    base_url : str
        API host.
    transport : str
        ``"grpc"`` (default) or ``"http"``.
    timeout : float
        Request timeout in seconds.
    use_tls : bool
        Use TLS for the connection.
    """

    api_key: str | None = None
    _token: str | None = None
    base_url: str = "grpc.sandbox.anedyacloud.com"
    transport: str = "grpc"
    grpc_port: int = 443
    http_base_path: str = "/v1"
    timeout: float = 30.0
    use_tls: bool = True
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # If no api_key was passed, check env vars
        if self.api_key is None:
            self.api_key = os.environ.get("ANEDYA_API_KEY")
        if self.api_key is None:
            self._token = os.environ.get("ANEDYA_SERVICE_TOKEN")

        if self.api_key is None and self._token is None:
            raise ValueError(
                "No credentials provided. Pass api_key= or token= to the client, "
                "or set ANEDYA_API_KEY / ANEDYA_SERVICE_TOKEN environment variable."
            )

    @property
    def grpc_target(self) -> str:
        host = self.base_url.replace("https://", "").replace("http://", "").rstrip("/")
        return f"{host}:{self.grpc_port}"

    @property
    def http_base_url(self) -> str:
        url = self.base_url
        if not url.startswith(("http://", "https://")):
            scheme = "https" if self.use_tls else "http"
            url = f"{scheme}://{url}"
        return url.rstrip("/") + self.http_base_path

    @property
    def auth_headers(self) -> dict[str, str]:
        credential = self.api_key or self._token
        auth_mode = "api_key" if self.api_key else "token"
        return {
            "authorization": f"Bearer {credential}",
            "x-anedya-auth-mode": auth_mode,
            **self.metadata,
        }
