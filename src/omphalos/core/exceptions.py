from __future__ import annotations

class WorkbenchError(Exception):
    """Base error."""

class ContractError(WorkbenchError):
    """Schema or contract validation failure."""

class GateError(WorkbenchError):
    """Gate failure."""

class DeterminismError(WorkbenchError):
    """Determinism verification or certification failure."""

class PublishabilityError(WorkbenchError):
    """Publishability scan failure."""

class ReleaseError(WorkbenchError):
    """Release bundle failure."""

class ArtifactError(WorkbenchError):
    """Artifact store failure."""

class ConfigError(WorkbenchError):
    """Configuration error."""
