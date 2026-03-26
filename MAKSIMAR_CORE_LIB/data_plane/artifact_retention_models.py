from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArtifactRetentionRule:
    """Canonical artifact retention rule."""

    artifact_type: str
    retention_days: int
    cleanup_allowed: bool


@dataclass(frozen=True, slots=True)
class ArtifactRetentionContract:
    """Unified artifact retention contract."""

    total_rules: int
    rules: tuple[ArtifactRetentionRule, ...]
