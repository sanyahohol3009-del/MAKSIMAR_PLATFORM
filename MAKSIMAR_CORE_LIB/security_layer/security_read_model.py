from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class SecurityReadModelStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class SecurityVerifierReadinessReadModel:
    verifier_id: str
    available: bool
    status: SecurityReadModelStatus
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.verifier_id:
            raise ValueError("verifier_id must not be empty")
        if not isinstance(self.status, SecurityReadModelStatus):
            raise TypeError("status must be SecurityReadModelStatus")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.available and self.status is SecurityReadModelStatus.BLOCKED:
            raise ValueError("available verifier cannot have BLOCKED status")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "verifier_id": self.verifier_id,
            "available": self.available,
            "status": self.status.value,
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
        }


@dataclass(frozen=True, slots=True)
class SecurityAdapterReadModel:
    adapter_id: str
    adapter_kind: str
    source_count: int
    status: SecurityReadModelStatus
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.adapter_id:
            raise ValueError("adapter_id must not be empty")
        if not self.adapter_kind:
            raise ValueError("adapter_kind must not be empty")
        if self.source_count < 0:
            raise ValueError("source_count must not be negative")
        if not isinstance(self.status, SecurityReadModelStatus):
            raise TypeError("status must be SecurityReadModelStatus")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_id": self.adapter_id,
            "adapter_kind": self.adapter_kind,
            "source_count": self.source_count,
            "status": self.status.value,
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
        }


@dataclass(frozen=True, slots=True)
class SecurityGateRuntimeReadModel:
    request_id: str
    trace_id: str
    decision_status: str
    risk_level: str
    decision_allows_execution: bool
    actual_execution_performed: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_dashboard_execution_allowed: bool = False

    def __post_init__(self) -> None:
        for field_name, value in (
            ("request_id", self.request_id),
            ("trace_id", self.trace_id),
            ("decision_status", self.decision_status),
            ("risk_level", self.risk_level),
        ):
            if not value:
                raise ValueError(f"{field_name} must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.actual_execution_performed:
            raise ValueError("security read model must never report actual execution")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_dashboard_execution_allowed:
            raise ValueError("direct_dashboard_execution_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "trace_id": self.trace_id,
            "decision_status": self.decision_status,
            "risk_level": self.risk_level,
            "decision_allows_execution": self.decision_allows_execution,
            "actual_execution_performed": self.actual_execution_performed,
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "direct_dashboard_execution_allowed": self.direct_dashboard_execution_allowed,
        }


@dataclass(frozen=True, slots=True)
class SecurityLayerHealthReadModel:
    layer_id: str
    status: SecurityReadModelStatus
    present_files: tuple[str, ...]
    missing_files: tuple[str, ...]
    verifier_readiness: tuple[SecurityVerifierReadinessReadModel, ...]
    adapter_readiness: tuple[SecurityAdapterReadModel, ...]
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.layer_id:
            raise ValueError("layer_id must not be empty")
        if not isinstance(self.status, SecurityReadModelStatus):
            raise TypeError("status must be SecurityReadModelStatus")
        if not isinstance(self.present_files, tuple):
            raise TypeError("present_files must be a tuple")
        if not isinstance(self.missing_files, tuple):
            raise TypeError("missing_files must be a tuple")
        if not isinstance(self.verifier_readiness, tuple):
            raise TypeError("verifier_readiness must be a tuple")
        if not isinstance(self.adapter_readiness, tuple):
            raise TypeError("adapter_readiness must be a tuple")
        for item in self.verifier_readiness:
            if not isinstance(item, SecurityVerifierReadinessReadModel):
                raise TypeError("verifier_readiness must contain SecurityVerifierReadinessReadModel")
        for item in self.adapter_readiness:
            if not isinstance(item, SecurityAdapterReadModel):
                raise TypeError("adapter_readiness must contain SecurityAdapterReadModel")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if self.missing_files and self.status is SecurityReadModelStatus.HEALTHY:
            raise ValueError("healthy status requires no missing files")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "status": self.status.value,
            "present_files": list(self.present_files),
            "missing_files": list(self.missing_files),
            "verifier_readiness": [item.to_dict() for item in self.verifier_readiness],
            "adapter_readiness": [item.to_dict() for item in self.adapter_readiness],
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
        }


@dataclass(frozen=True, slots=True)
class SecurityTelemetryReadModel:
    layer_id: str
    batch_id: str
    status: SecurityReadModelStatus
    gate: SecurityGateRuntimeReadModel
    health: SecurityLayerHealthReadModel
    generated_by: str
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.layer_id:
            raise ValueError("layer_id must not be empty")
        if not self.batch_id:
            raise ValueError("batch_id must not be empty")
        if not isinstance(self.status, SecurityReadModelStatus):
            raise TypeError("status must be SecurityReadModelStatus")
        if not isinstance(self.gate, SecurityGateRuntimeReadModel):
            raise TypeError("gate must be SecurityGateRuntimeReadModel")
        if not isinstance(self.health, SecurityLayerHealthReadModel):
            raise TypeError("health must be SecurityLayerHealthReadModel")
        if not self.generated_by:
            raise ValueError("generated_by must not be empty")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "batch_id": self.batch_id,
            "status": self.status.value,
            "gate": self.gate.to_dict(),
            "health": self.health.to_dict(),
            "generated_by": self.generated_by,
            "reason_codes": list(self.reason_codes),
            "dashboard_safe": self.dashboard_safe,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
        }
