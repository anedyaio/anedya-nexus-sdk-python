"""AnedyaClient — main entry point for the SDK.

Usage::

    from anedya.sdk import AnedyaClient, VariableReading

    # Explicit API key
    with AnedyaClient(api_key="your-key") as client:
        client.data_management.submit_data([...])

    # From env (ANEDYA_API_KEY or ANEDYA_SERVICE_TOKEN)
    with AnedyaClient() as client:
        client.data_management.submit_data([...])

    # HTTP transport
    with AnedyaClient(api_key="your-key", transport="http") as client:
        client.data_management.submit_data([...])
"""

from anedya.sdk._transport.grpc import GrpcTransport
from anedya.sdk._transport.http import HttpTransport
from anedya.sdk.config import ClientConfig
from anedya.sdk.services.data_management import DatamanagementService


class AnedyaClient:
    """SDK client. Uses gRPC by default, HTTP if you pass ``transport="http"``.

    Authentication is resolved in this order:
        1. Explicit ``api_key`` parameter
        2. ``ANEDYA_API_KEY`` environment variable
        3. ``ANEDYA_SERVICE_TOKEN`` environment variable

    Parameters
    ----------
    api_key : str, optional
        Anedya API key.
    base_url : str
        API host. Defaults to ``api.anedya.io``.
    transport : str
        ``"grpc"`` (default) or ``"http"``.
    **kwargs
        Extra options passed to :class:`ClientConfig`.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "grpc.sandbox.anedyacloud.com", # TODO: Region code or full url
        transport: str = "grpc",
        **kwargs,
    ) -> None:
        self._config = ClientConfig(
            api_key=api_key,
            base_url=base_url,
            transport=transport,
            **kwargs,
        )

        # Pick the right transport
        if self._config.transport == "http":
            self._transport = HttpTransport(self._config)
        else:
            self._transport = GrpcTransport(self._config)

        # Services
        self.data_management = DatamanagementService(self._transport)

    def connect(self) -> None:
        """Open the connection."""
        self._transport.connect()

    def close(self) -> None:
        """Close the connection."""
        self._transport.close()

    # Context manager
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *exc):
        self.close()
