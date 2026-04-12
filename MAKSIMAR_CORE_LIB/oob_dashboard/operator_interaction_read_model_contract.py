from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_contract import (
    build_operator_control_plane_handoff_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_contract import (
    build_operator_intent_contract,
)

InteractionLane = Literal[
    "read_only_lane",
    "approval_bound_lane",
]

InteractionSurfaceState = Literal[
    "read_only_interaction_surface",
    "approval_bound_interaction_surface",
]

ALL_INTERACTION_LANES: tuple[InteractionLane, ...] = (
    "read_only_lane",
    "approval_bound_lane",
)

ALL_INTERACTION_SURFACE_STATES: tuple[InteractionSurfaceState, ...] = (
    "read_only_interaction_surface",
    "approval_bound_interaction_surface",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorInteractionReadModelEntry:
    """Canonical operator interaction read-model entry."""

    operator_intent_id: str
    dashboard_id: str
    workspace_id: str
    interaction_lane: InteractionLane
    interaction_surface_state: InteractionSurfaceState
    intent_kind: str
    approval_state: str
    handoff_state: str
    audit_visibility_state: str
    approval_required: bool
    handoff_ready: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator interaction read-model entry."""
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.intent_kind, "intent_kind")
        _require_non_empty(self.approval_state, "approval_state")
        _require_non_empty(self.handoff_state, "handoff_state")
        _require_non_empty(self.audit_visibility_state, "audit_visibility_state")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.interaction_lane not in ALL_INTERACTION_LANES:
            raise ValueError(
                f"interaction_lane must be one of {ALL_INTERACTION_LANES}, "
                f"got {self.interaction_lane!r}."
            )

        if self.interaction_surface_state not in ALL_INTERACTION_SURFACE_STATES:
            raise ValueError(
                "interaction_surface_state must be one of "
                f"{ALL_INTERACTION_SURFACE_STATES}, "
                f"got {self.interaction_surface_state!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical "
                "operator interaction read-model entries."
            )

        if self.interaction_lane == "read_only_lane":
            if self.approval_required:
                raise ValueError(
                    "read_only_lane entries must not require approval."
                )
            if self.interaction_surface_state != "read_only_interaction_surface":
                raise ValueError(
                    "read_only_lane entries must use "
                    "read_only_interaction_surface."
                )

        if self.interaction_lane == "approval_bound_lane":
            if not self.approval_required:
                raise ValueError(
                    "approval_bound_lane entries must require approval."
                )
            if (
                self.interaction_surface_state
                != "approval_bound_interaction_surface"
            ):
                raise ValueError(
                    "approval_bound_lane entries must use "
                    "approval_bound_interaction_surface."
                )

        if self.handoff_ready != (self.handoff_state == "handoff_ready"):
            raise ValueError(
                "handoff_ready must reflect whether handoff_state is "
                "handoff_ready."
            )


@dataclass(frozen=True, slots=True)
class OperatorInteractionReadModelContract:
    """Canonical operator interaction read-model contract."""

    contract_id: str
    total_entries: int
    read_only_lane_entries: int
    approval_bound_lane_entries: int
    approval_required_entries: int
    handoff_ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorInteractionReadModelEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator interaction read-model contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.read_only_lane_entries != sum(
            1 for entry in self.entries if entry.interaction_lane == "read_only_lane"
        ):
            raise ValueError(
                "read_only_lane_entries must match read_only_lane count."
            )

        if self.approval_bound_lane_entries != sum(
            1
            for entry in self.entries
            if entry.interaction_lane == "approval_bound_lane"
        ):
            raise ValueError(
                "approval_bound_lane_entries must match approval_bound_lane count."
            )

        if self.approval_required_entries != sum(
            1 for entry in self.entries if entry.approval_required
        ):
            raise ValueError(
                "approval_required_entries must match approval_required count."
            )

        if self.handoff_ready_entries != sum(
            1 for entry in self.entries if entry.handoff_ready
        ):
            raise ValueError(
                "handoff_ready_entries must match handoff_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_interaction_read_model_contract() -> (
    OperatorInteractionReadModelContract
):
    """Build canonical operator interaction read-model contract.

    After the visual/operator demolition pass, this read model is intentionally
    derived only from:
    - operator intent truth
    - operator control-plane handoff truth

    Approval/audit-specific layers were removed from the active spine and must
    not be pulled back in here.
    """
    intent_contract = build_operator_intent_contract()
    handoff_contract = build_operator_control_plane_handoff_contract()

    handoff_by_intent = {
        entry.operator_intent_id: entry
        for entry in handoff_contract.entries
    }

    entries = tuple(
        OperatorInteractionReadModelEntry(
            operator_intent_id=intent_entry.operator_intent_id,
            dashboard_id=intent_entry.dashboard_id,
            workspace_id=intent_entry.workspace_id,
            interaction_lane=(
                "approval_bound_lane"
                if intent_entry.approval_required
                else "read_only_lane"
            ),
            interaction_surface_state=(
                "approval_bound_interaction_surface"
                if intent_entry.approval_required
                else "read_only_interaction_surface"
            ),
            intent_kind=intent_entry.intent_kind,
            approval_state=(
                "approval_required"
                if intent_entry.approval_required
                else "approval_not_required"
            ),
            handoff_state=handoff_by_intent[
                intent_entry.operator_intent_id
            ].handoff_state,
            audit_visibility_state="audit_layer_removed_from_active_spine",
            approval_required=intent_entry.approval_required,
            handoff_ready=(
                handoff_by_intent[intent_entry.operator_intent_id].handoff_state
                == "handoff_ready"
            ),
            operator_visible=True,
            trace_id=intent_entry.trace_id,
            description=(
                "Canonical operator interaction read-model entry for "
                f"{intent_entry.operator_intent_id}."
            ),
        )
        for intent_entry in intent_contract.entries
    )

    return OperatorInteractionReadModelContract(
        contract_id="operator_interaction_read_model_contract_001",
        total_entries=len(entries),
        read_only_lane_entries=sum(
            1 for entry in entries if entry.interaction_lane == "read_only_lane"
        ),
        approval_bound_lane_entries=sum(
            1
            for entry in entries
            if entry.interaction_lane == "approval_bound_lane"
        ),
        approval_required_entries=sum(
            1 for entry in entries if entry.approval_required
        ),
        handoff_ready_entries=sum(1 for entry in entries if entry.handoff_ready),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
