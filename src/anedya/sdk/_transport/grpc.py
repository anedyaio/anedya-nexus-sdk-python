"""gRPC transport — the default transport for the SDK."""

import grpc
from google.protobuf.message import Message as ProtoMessage

from anedya.sdk.config import ClientConfig
from anedya.sdk.errors import ConnectionError, TransportError


class GrpcTransport:
    """Sync gRPC transport."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._channel: grpc.Channel | None = None

    def connect(self) -> None:
        if self._channel is not None:
            return

        target = self._config.grpc_target
        metadata = list(self._config.auth_headers.items())

        if self._config.use_tls:
            credentials = grpc.ssl_channel_credentials()
            auth_creds = grpc.metadata_call_credentials(
                _AuthPlugin(metadata),
            )
            composite = grpc.composite_channel_credentials(credentials, auth_creds)
            self._channel = grpc.secure_channel(target, composite)
        else:
            self._channel = grpc.insecure_channel(target)

    def close(self) -> None:
        if self._channel is not None:
            self._channel.close()
            self._channel = None

    def unary(
        self,
        service: str,
        method: str,
        request: ProtoMessage,
        response_type: type[ProtoMessage],
        timeout: float | None = None,
    ) -> ProtoMessage:
        """Make a unary RPC call."""
        if self._channel is None:
            raise ConnectionError("Not connected. Call connect() first.")

        rpc_path = f"/{service}/{method}"
        call = self._channel.unary_unary(
            rpc_path,
            request_serializer=type(request).SerializeToString,
            response_deserializer=response_type.FromString,
        )

        try:
            return call(request, timeout=timeout or self._config.timeout)
        except grpc.RpcError as e:
            raise TransportError(f"gRPC error: {e}") from e


class _AuthPlugin(grpc.AuthMetadataPlugin):
    """Injects auth metadata into every gRPC call."""

    def __init__(self, metadata: list[tuple[str, str]]) -> None:
        self._metadata = metadata

    def __call__(self, context, callback) -> None:
        callback(self._metadata, None)
