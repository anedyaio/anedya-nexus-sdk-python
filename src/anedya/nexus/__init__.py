"""Anedya Nexus SDK for Python.

Usage::

    from anedya.nexus import AnedyaClient, VariableReading

    with AnedyaClient(api_key="your-key") as client:
        client.data_management.submit_data([
            VariableReading(variable="temp", timestamp=1700000000000, float_value=23.5),
        ])
"""

from .client import AnedyaClient
from .config import ClientConfig
from .errors import AnedyaError, AuthenticationError, ConnectionError, TimeoutError, TransportError
from .models.common import GeoData, VariableReading

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
