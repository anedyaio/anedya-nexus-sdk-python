"""Custom exceptions for the Anedya SDK."""


class AnedyaError(Exception):
    """Base exception for all SDK errors."""


class AuthenticationError(AnedyaError):
    """Invalid or missing API key."""


class ConnectionError(AnedyaError):
    """Cannot connect to the API."""


class TimeoutError(AnedyaError):
    """Request timed out."""


class TransportError(AnedyaError):
    """Transport-level failure (bad status code, etc.)."""
