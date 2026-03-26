from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AdmissionRuntimeState:
    """Canonical admission runtime state entry."""

    request_id: str
    admitted: bool
    denial_reason: str
    policy_checked: bool


@dataclass(frozen=True, slots=True)
class AdmissionRuntimeContract:
    """Unified admission runtime state contract."""

    total_requests: int
    requests: tuple[AdmissionRuntimeState, ...]
