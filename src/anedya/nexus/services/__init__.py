"""Services."""

from anedya.nexus.services.data_management import DatamanagementService

# Backward compatibility alias
IngestService = DatamanagementService

__all__ = ["DatamanagementService", "IngestService"]
