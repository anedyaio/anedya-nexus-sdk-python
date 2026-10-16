"""Data models for the SDK."""

from dataclasses import dataclass


@dataclass
class GeoData:
    """Geographic coordinates."""
    lat: float = 0.0
    long: float = 0.0
    latitude: float | None = None
    longitude: float | None = None

    def __post_init__(self) -> None:
        if self.latitude is not None:
            self.lat = self.latitude
        else:
            self.latitude = self.lat
        if self.longitude is not None:
            self.long = self.longitude
        else:
            self.longitude = self.long


@dataclass
class VariableReading:
    """A single variable reading to submit.

    Set exactly one of float_value, string_value, or geo_data.
    """
    variable: str
    timestamp: int
    float_value: float | None = None
    string_value: str | None = None
    geo_data: GeoData | None = None
    node_id: str | None = None
