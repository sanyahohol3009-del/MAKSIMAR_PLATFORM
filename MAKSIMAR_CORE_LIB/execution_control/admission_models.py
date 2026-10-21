from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    """Canonical admission control decision."""

    request_id: str
    admitted: bool
    reason: str
    policy_checked: bool
    model_id: str = ""
    role_id: str = ""
    resource_evidence: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class AdmissionContract:
    """Unified admission control contract."""

    total_decisions: int
    decisions: tuple[AdmissionDecision, ...]


@dataclass(frozen=True, slots=True)
class ModelResourceObservation:
    """Request-local facts from trusted adapters; no lease/store authority.

    Memory domains are simultaneous independent constraints, never additive.
    Provider residency alone cannot set ownership_verified or active_concurrency.
    """

    observed_monotonic: float
    backend_id: str
    scope_id: str
    provider_instance_id: str
    provider_available: bool
    model_revision: str
    memory_available_bytes: tuple[tuple[str, int], ...]
    accelerator_available_bytes: tuple[tuple[str, int], ...]
    cpu_threads: int
    physical_identity_verified: bool
    scope_confirmed: bool
    ownership_verified: bool
    ownership_source: str
    active_concurrency: int | None
    resident_models: tuple[tuple[str, str], ...]
    complete: bool
    source: str
