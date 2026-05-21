from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ModelProvenanceContract:
    provenance_id: str
    model_id: str
    model_family: str
    route_reason: str
    source_binding_ref: str
    provenance_ready: bool
    canonical_evidence_memory_write_allowed: bool
    model_runtime_execution_allowed: bool
    runtime_mutation_allowed: bool
    dashboard_safe: bool
    read_only: bool
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        _validate_non_empty("provenance_id", self.provenance_id)
        _validate_non_empty("model_id", self.model_id)
        _validate_non_empty("model_family", self.model_family)
        _validate_non_empty("route_reason", self.route_reason)
        _validate_non_empty("source_binding_ref", self.source_binding_ref)
        _validate_true("provenance_ready", self.provenance_ready)
        _validate_false("canonical_evidence_memory_write_allowed", self.canonical_evidence_memory_write_allowed)
        _validate_false("model_runtime_execution_allowed", self.model_runtime_execution_allowed)
        _validate_false("runtime_mutation_allowed", self.runtime_mutation_allowed)
        _validate_true("dashboard_safe", self.dashboard_safe)
        _validate_true("read_only", self.read_only)
        _validate_non_empty_tuple("reason_codes", self.reason_codes)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance_id": self.provenance_id,
            "model_id": self.model_id,
            "model_family": self.model_family,
            "route_reason": self.route_reason,
            "source_binding_ref": self.source_binding_ref,
            "provenance_ready": self.provenance_ready,
            "canonical_evidence_memory_write_allowed": self.canonical_evidence_memory_write_allowed,
            "model_runtime_execution_allowed": self.model_runtime_execution_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "dashboard_safe": self.dashboard_safe,
            "read_only": self.read_only,
            "reason_codes": self.reason_codes,
        }


def build_default_model_provenance_contract() -> ModelProvenanceContract:
    return ModelProvenanceContract(
        provenance_id="model_provenance_v1",
        model_id="existing_ai_router_selected_model",
        model_family="existing_ai_services_binding",
        route_reason="existing_ai_router_binding_reference",
        source_binding_ref="AI_ORCHESTRATION/existing_bindings/ai_services_binding.yaml",
        provenance_ready=True,
        canonical_evidence_memory_write_allowed=False,
        model_runtime_execution_allowed=False,
        runtime_mutation_allowed=False,
        dashboard_safe=True,
        read_only=True,
        reason_codes=(
            "model_provenance_contract_only",
            "canonical_evidence_memory_write_blocked",
            "runtime_execution_blocked",
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
