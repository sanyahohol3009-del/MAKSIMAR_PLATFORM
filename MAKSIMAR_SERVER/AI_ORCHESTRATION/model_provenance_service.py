from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.ai_orchestration import (
    ModelProvenanceContract,
    build_default_model_provenance_contract,
)


@dataclass(frozen=True, slots=True)
class ModelProvenanceServiceReadModel:
    service_id: str
    provenance_contract: ModelProvenanceContract
    provenance_ready: bool
    canonical_evidence_memory_write_allowed: bool
    model_runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("service_id", self.service_id)
        if not isinstance(self.provenance_contract, ModelProvenanceContract):
            raise TypeError("provenance_contract must be ModelProvenanceContract")
        _validate_true("provenance_ready", self.provenance_ready)
        _validate_false("canonical_evidence_memory_write_allowed", self.canonical_evidence_memory_write_allowed)
        _validate_false("model_runtime_execution_allowed", self.model_runtime_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "provenance_contract": self.provenance_contract.to_dict(),
            "provenance_ready": self.provenance_ready,
            "canonical_evidence_memory_write_allowed": self.canonical_evidence_memory_write_allowed,
            "model_runtime_execution_allowed": self.model_runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_model_provenance_service_read_model() -> ModelProvenanceServiceReadModel:
    contract = build_default_model_provenance_contract()
    return ModelProvenanceServiceReadModel(
        service_id="model_provenance_service_v1",
        provenance_contract=contract,
        provenance_ready=contract.provenance_ready,
        canonical_evidence_memory_write_allowed=False,
        model_runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "model_provenance_service_read_model_only",
            "canonical_evidence_write_blocked",
            "model_runtime_execution_blocked",
        ),
    )


def _validate_non_empty(field_name: str, value: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if not value:
        raise ValueError(f"{field_name} must not be empty")


def _validate_true(field_name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain true")


def _validate_false(field_name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain false")


def _validate_non_empty_tuple(field_name: str, value: tuple[str, ...]) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    for item in value:
        _validate_non_empty(field_name, item)
