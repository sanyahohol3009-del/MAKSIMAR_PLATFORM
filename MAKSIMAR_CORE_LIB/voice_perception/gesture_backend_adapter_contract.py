from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_BINDS_TO_EXISTING_SURFACES = (
    "MAKSIMAR_CORE_LIB/oob_dashboard/gesture_input_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/gesture_adapter_contract.py",
    "MAKSIMAR_CORE_LIB/oob_dashboard/gesture_policy_handoff_contract.py",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")


@dataclass(frozen=True, slots=True)
class GestureBackendAdapterContract:
    contract_id: str
    adapter_kind: str
    input_payload_kind: str
    output_payload_kind: str
    gesture_intent_candidate_only: bool = True
    direct_action_allowed: bool = False
    direct_mobile_control_allowed: bool = False
    pc_control_allowed: bool = False
    shell_execution_allowed: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    always_listening_allowed: bool = False
    proposal_only: bool = True
    binds_to_existing_surfaces: tuple[str, ...] = _BINDS_TO_EXISTING_SURFACES

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.adapter_kind, "adapter_kind")
        _require_non_empty(self.input_payload_kind, "input_payload_kind")
        _require_non_empty(self.output_payload_kind, "output_payload_kind")
        _require_true(self.gesture_intent_candidate_only, "gesture_intent_candidate_only")
        _require_false(self.direct_action_allowed, "direct_action_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.always_listening_allowed, "always_listening_allowed")
        _require_true(self.proposal_only, "proposal_only")
        if self.binds_to_existing_surfaces != _BINDS_TO_EXISTING_SURFACES:
            raise ValueError(
                "binds_to_existing_surfaces must match canonical gesture bindings"
            )
        if self.input_payload_kind != "gesture_candidate_metadata":
            raise ValueError("input_payload_kind must remain gesture_candidate_metadata")
        if self.output_payload_kind != "gesture_intent_candidate":
            raise ValueError("output_payload_kind must remain gesture_intent_candidate")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "adapter_kind": self.adapter_kind,
            "input_payload_kind": self.input_payload_kind,
            "output_payload_kind": self.output_payload_kind,
            "gesture_intent_candidate_only": self.gesture_intent_candidate_only,
            "direct_action_allowed": self.direct_action_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "always_listening_allowed": self.always_listening_allowed,
            "proposal_only": self.proposal_only,
            "binds_to_existing_surfaces": self.binds_to_existing_surfaces,
        }


def build_gesture_backend_adapter_contract() -> GestureBackendAdapterContract:
    return GestureBackendAdapterContract(
        contract_id="gesture_backend_adapter_contract_v0_1",
        adapter_kind="gesture_backend_adapter",
        input_payload_kind="gesture_candidate_metadata",
        output_payload_kind="gesture_intent_candidate",
    )
