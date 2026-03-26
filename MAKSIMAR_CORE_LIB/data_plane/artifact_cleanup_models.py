from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ArtifactCleanupRule:
    """Canonical artifact cleanup rule."""

    artifact_type: str
    cleanup_strategy: str
    approval_required: bool


@dataclass(frozen=True, slots=True)
class ArtifactCleanupContract:
    """Unified artifact cleanup contract."""

    total_rules: int
    rules: tuple[ArtifactCleanupRule, ...]
