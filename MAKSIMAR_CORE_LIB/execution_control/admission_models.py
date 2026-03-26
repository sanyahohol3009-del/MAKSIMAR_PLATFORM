from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    """Canonical admission control decision."""

    request_id: str
    admitted: bool
    reason: str
    policy_checked: bool


@dataclass(frozen=True, slots=True)
class AdmissionContract:
    """Unified admission control contract."""

    total_decisions: int
    decisions: tuple[AdmissionDecision, ...]
