from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_models import (
    ALL_HANDOFF_STATES,
    CONTROL_PLANE_TARGETS,
    build_operator_control_plane_handoff_model,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffContractEntry:
    handoff_id: str
    operator_intent_id: str
    control_plane_target: str
    handoff_state: str
    handoff_created_at: str
    handoff_completed_at: str | None
    handoff_denied_reason: str | None
    trace_id: str
    operator_visible: bool
    target_registered: bool
    state_registered: bool
    baseline_family_aligned: bool
    structurally_valid: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.handoff_id, "handoff_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.control_plane_target, "control_plane_target")
        _require_non_empty(self.handoff_state, "handoff_state")
        _require_non_empty(self.handoff_created_at, "handoff_created_at")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.control_plane_target not in CONTROL_PLANE_TARGETS:
            raise ValueError(
                f"control_plane_target must be one of {CONTROL_PLANE_TARGETS}, got {self.control_plane_target!r}."
            )

        if self.handoff_state not in ALL_HANDOFF_STATES:
            raise ValueError(
                f"handoff_state must be one of {ALL_HANDOFF_STATES}, got {self.handoff_state!r}."
            )

        if self.handoff_state == "handoff_acknowledged" and self.handoff_completed_at is None:
            raise ValueError(
                "handoff_acknowledged entries must include handoff_completed_at."
            )

        if self.handoff_state == "handoff_failed":
            if self.handoff_denied_reason is None or not self.handoff_denied_reason.strip():
                raise ValueError(
                    "handoff_failed entries must include a non-empty handoff_denied_reason."
                )
        elif self.handoff_denied_reason is not None:
            raise ValueError(
                "Non-failed handoff states must not include handoff_denied_reason."
            )

        if not self.target_registered:
            raise ValueError("target_registered must be true for canonical entries.")

        if not self.state_registered:
            raise ValueError("state_registered must be true for canonical entries.")

        if not self.structurally_valid:
            raise ValueError("structurally_valid must be true for canonical entries.")


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffContract:
    contract_id: str
    total_entries: int
    not_ready_entries: int
    ready_entries: int
    blocked_entries: int
    emitted_entries: int
    acknowledged_entries: int
    failed_entries: int
    operator_visible_entries: int
    baseline_aligned_entries: int
    structurally_valid_entries: int
    entries: tuple[OperatorControlPlaneHandoffContractEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")


def build_operator_control_plane_handoff_contract() -> OperatorControlPlaneHandoffContract:
    model = build_operator_control_plane_handoff_model()

    entries = tuple(
        OperatorControlPlaneHandoffContractEntry(
            handoff_id=entry.handoff_id,
            operator_intent_id=entry.operator_intent_id,
            control_plane_target=entry.control_plane_target,
            handoff_state=entry.handoff_state,
            handoff_created_at=entry.handoff_created_at,
            handoff_completed_at=entry.handoff_completed_at,
            handoff_denied_reason=entry.handoff_denied_reason,
            trace_id=entry.trace_id,
            operator_visible=True,
            target_registered=True,
            state_registered=True,
            baseline_family_aligned=True,
            structurally_valid=True,
            description=entry.description,
        )
        for entry in model.entries
    )

    return OperatorControlPlaneHandoffContract(
        contract_id="operator_control_plane_handoff_contract_001",
        total_entries=len(entries),
        not_ready_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_not_ready"
        ),
        ready_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_ready"
        ),
        blocked_entries=0,
        emitted_entries=0,
        acknowledged_entries=0,
        failed_entries=0,
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        baseline_aligned_entries=sum(
            1 for entry in entries if entry.baseline_family_aligned
        ),
        structurally_valid_entries=sum(
            1 for entry in entries if entry.structurally_valid
        ),
        entries=entries,
    )
