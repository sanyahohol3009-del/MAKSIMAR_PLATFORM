from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    build_operator_intent_model,
)

ALL_HANDOFF_STATES: tuple[str, ...] = (
    "handoff_not_ready",
    "handoff_ready",
    "handoff_blocked",
    "handoff_emitted",
    "handoff_acknowledged",
    "handoff_failed",
)

CONTROL_PLANE_TARGETS: tuple[str, ...] = (
    "control_plane_operator_router",
    "control_plane_policy_gate",
    "control_plane_execution_intake",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffEntry:
    handoff_id: str
    operator_intent_id: str
    control_plane_target: str
    handoff_state: str
    handoff_created_at: str
    handoff_completed_at: str | None
    handoff_denied_reason: str | None
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.handoff_id, "handoff_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.control_plane_target, "control_plane_target")
        _require_non_empty(self.handoff_state, "handoff_state")
        _require_non_empty(self.handoff_created_at, "handoff_created_at")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.handoff_state not in ALL_HANDOFF_STATES:
            raise ValueError(
                f"handoff_state must be one of {ALL_HANDOFF_STATES}, got {self.handoff_state!r}."
            )

        if self.control_plane_target not in CONTROL_PLANE_TARGETS:
            raise ValueError(
                f"control_plane_target must be one of {CONTROL_PLANE_TARGETS}, got {self.control_plane_target!r}."
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


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffModel:
    model_id: str
    total_entries: int
    handoff_not_ready_entries: int
    handoff_ready_entries: int
    handoff_blocked_entries: int
    handoff_emitted_entries: int
    handoff_acknowledged_entries: int
    handoff_failed_entries: int
    entries: tuple[OperatorControlPlaneHandoffEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.model_id, "model_id")
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")


def build_operator_control_plane_handoff_model() -> OperatorControlPlaneHandoffModel:
    """Build canonical handoff model expected by smoke tests."""
    intent_model = build_operator_intent_model()
    intent_by_id = {entry.operator_intent_id: entry for entry in intent_model.entries}

    entries = (
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_001",
            operator_intent_id="operator_intent_001",
            control_plane_target="control_plane_operator_router",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id=intent_by_id["operator_intent_001"].trace_id,
            description="Canonical view-only handoff entry.",
        ),
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_002",
            operator_intent_id="operator_intent_002",
            control_plane_target="control_plane_operator_router",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id=intent_by_id["operator_intent_002"].trace_id,
            description="Canonical navigation handoff entry kept non-executing.",
        ),
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_003",
            operator_intent_id="operator_intent_003",
            control_plane_target="control_plane_policy_gate",
            handoff_state="handoff_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id=intent_by_id["operator_intent_003"].trace_id,
            description="Canonical approval-bound control handoff entry.",
        ),
    )

    return OperatorControlPlaneHandoffModel(
        model_id="operator_control_plane_handoff_model_001",
        total_entries=len(entries),
        handoff_not_ready_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_not_ready"
        ),
        handoff_ready_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_ready"
        ),
        handoff_blocked_entries=0,
        handoff_emitted_entries=0,
        handoff_acknowledged_entries=0,
        handoff_failed_entries=0,
        entries=entries,
    )
