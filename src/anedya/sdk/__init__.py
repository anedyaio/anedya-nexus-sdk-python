"""Anedya SDK for Python.

Usage::

    from anedya.sdk import AnedyaClient, VariableReading

    with AnedyaClient(api_key="your-key") as client:
        client.data_management.submit_data([
            VariableReading(variable="temp", timestamp=1700000000000, float_value=23.5),
        ])
"""

from anedya.sdk.client import AnedyaClient
from anedya.sdk.config import ClientConfig
from anedya.sdk.errors import AnedyaError, AuthenticationError, ConnectionError, TimeoutError, TransportError
from anedya.sdk.models.common import GeoData, VariableReading

__all__ = [
    "AnedyaClient",
    "ClientConfig",
    "GeoData",
    "VariableReading",
    "AnedyaError",
    "AuthenticationError",
    "ConnectionError",
    "TimeoutError",
    "TransportError",
]
