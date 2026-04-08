from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_decision_models import (
    build_operator_approval_decision_model,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    build_operator_intent_model,
)


HandoffState = Literal[
    "handoff_not_ready",
    "handoff_ready",
    "handoff_blocked",
    "handoff_emitted",
    "handoff_acknowledged",
    "handoff_failed",
]

ALL_HANDOFF_STATES: tuple[HandoffState, ...] = (
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
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffEntry:
    """Canonical operator control-plane handoff entry.

    This model represents the handoff boundary between dashboard/operator
    interaction surfaces and downstream control-plane orchestration. A handoff
    entry is not execution itself; it is only the canonical transfer state.
    """

    handoff_id: str
    operator_intent_id: str
    control_plane_target: str
    handoff_state: HandoffState
    handoff_created_at: str
    handoff_completed_at: str | None
    handoff_denied_reason: str | None
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator control-plane handoff entry fields."""
        _require_non_empty(self.handoff_id, "handoff_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.control_plane_target, "control_plane_target")
        _require_non_empty(self.handoff_created_at, "handoff_created_at")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.handoff_state not in ALL_HANDOFF_STATES:
            raise ValueError(
                f"handoff_state must be one of {ALL_HANDOFF_STATES}, got {self.handoff_state!r}."
            )

        if self.control_plane_target not in CONTROL_PLANE_TARGETS:
            raise ValueError(
                "control_plane_target must be one of "
                f"{CONTROL_PLANE_TARGETS}, got {self.control_plane_target!r}."
            )

        if self.handoff_state == "handoff_acknowledged" and self.handoff_completed_at is None:
            raise ValueError(
                "handoff_acknowledged entries must include handoff_completed_at."
            )

        if self.handoff_state == "handoff_failed" and (
            self.handoff_denied_reason is None or not self.handoff_denied_reason.strip()
        ):
            raise ValueError(
                "handoff_failed entries must include a non-empty handoff_denied_reason."
            )

        if self.handoff_state in {"handoff_not_ready", "handoff_ready", "handoff_emitted"}:
            if self.handoff_denied_reason is not None:
                raise ValueError(
                    "Non-failed handoff states must not include handoff_denied_reason."
                )


@dataclass(frozen=True, slots=True)
class OperatorControlPlaneHandoffModel:
    """Canonical operator control-plane handoff model."""

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
        """Validate canonical operator control-plane handoff model fields."""
        _require_non_empty(self.model_id, "model_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the model."
            )

        if self.handoff_not_ready_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_not_ready"
        ):
            raise ValueError(
                "handoff_not_ready_entries must match handoff_not_ready count."
            )

        if self.handoff_ready_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_ready"
        ):
            raise ValueError(
                "handoff_ready_entries must match handoff_ready count."
            )

        if self.handoff_blocked_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_blocked"
        ):
            raise ValueError(
                "handoff_blocked_entries must match handoff_blocked count."
            )

        if self.handoff_emitted_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_emitted"
        ):
            raise ValueError(
                "handoff_emitted_entries must match handoff_emitted count."
            )

        if self.handoff_acknowledged_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_acknowledged"
        ):
            raise ValueError(
                "handoff_acknowledged_entries must match handoff_acknowledged count."
            )

        if self.handoff_failed_entries != sum(
            1 for entry in self.entries if entry.handoff_state == "handoff_failed"
        ):
            raise ValueError(
                "handoff_failed_entries must match handoff_failed count."
            )


def build_operator_control_plane_handoff_model() -> OperatorControlPlaneHandoffModel:
    """Build canonical operator control-plane handoff model."""
    intent_model = build_operator_intent_model()
    approval_model = build_operator_approval_decision_model()

    intent_entries = {entry.operator_intent_id: entry for entry in intent_model.entries}
    approval_entries = {
        entry.operator_intent_id: entry for entry in approval_model.entries
    }

    entries = (
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_001",
            operator_intent_id="operator_intent_001",
            control_plane_target="control_plane_operator_router",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id=intent_entries["operator_intent_001"].trace_id,
            description=(
                "Canonical handoff baseline for a view-only operator intent that "
                "remains non-handoff and non-executing."
            ),
        ),
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_002",
            operator_intent_id="operator_intent_002",
            control_plane_target="control_plane_operator_router",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id=intent_entries["operator_intent_002"].trace_id,
            description=(
                "Canonical handoff baseline for a navigation operator intent that "
                "remains visible but not emitted into execution."
            ),
        ),
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_003",
            operator_intent_id="operator_intent_003",
            control_plane_target="control_plane_policy_gate",
            handoff_state="handoff_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id=approval_entries["operator_intent_003"].trace_id,
            description=(
                "Canonical handoff baseline for an approval-bound control intent "
                "that is ready for gated control-plane transfer but not executed."
            ),
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
        handoff_blocked_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_blocked"
        ),
        handoff_emitted_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_emitted"
        ),
        handoff_acknowledged_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_acknowledged"
        ),
        handoff_failed_entries=sum(
            1 for entry in entries if entry.handoff_state == "handoff_failed"
        ),
        entries=entries,
    )
