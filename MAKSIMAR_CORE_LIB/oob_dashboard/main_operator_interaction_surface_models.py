from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MainOperatorInteractionSurfaceState = Literal[
    "interaction_surface_ready",
]
MainOperatorInteractionSurfaceClass = Literal[
    "read_only_surface",
    "approval_bound_surface",
]

ALL_MAIN_OPERATOR_INTERACTION_SURFACE_STATES: tuple[
    MainOperatorInteractionSurfaceState, ...
] = (
    "interaction_surface_ready",
)
ALL_MAIN_OPERATOR_INTERACTION_SURFACE_CLASSES: tuple[
    MainOperatorInteractionSurfaceClass, ...
] = (
    "read_only_surface",
    "approval_bound_surface",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class MainOperatorInteractionSurfaceEntry:
    """Canonical main-operator interaction surface entry."""

    interaction_surface_id: str
    operator_intent_id: str
    dashboard_id: str
    workspace_id: str
    surface_state: MainOperatorInteractionSurfaceState
    surface_class: MainOperatorInteractionSurfaceClass
    intent_kind: Literal["view_request", "navigation_request", "control_request"]
    action_visible: bool
    disabled_state_visible: bool
    forbidden_state_visible: bool
    pending_approval_visible: bool
    approval_required: bool
    handoff_ready: bool
    audit_visible: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        """Validate canonical main-operator interaction surface entry."""
        _require_non_empty(self.interaction_surface_id, "interaction_surface_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.surface_state not in ALL_MAIN_OPERATOR_INTERACTION_SURFACE_STATES:
            raise ValueError(
                "surface_state must be one of "
                f"{ALL_MAIN_OPERATOR_INTERACTION_SURFACE_STATES}, "
                f"got {self.surface_state!r}."
            )

        if self.surface_class not in ALL_MAIN_OPERATOR_INTERACTION_SURFACE_CLASSES:
            raise ValueError(
                "surface_class must be one of "
                f"{ALL_MAIN_OPERATOR_INTERACTION_SURFACE_CLASSES}, "
                f"got {self.surface_class!r}."
            )

        if self.intent_kind not in {
            "view_request",
            "navigation_request",
            "control_request",
        }:
            raise ValueError(
                "intent_kind must be one of "
                "{'view_request', 'navigation_request', 'control_request'}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical interaction surface entries."
            )

        if not self.action_visible:
            raise ValueError(
                "action_visible must remain true for canonical interaction surface entries."
            )

        if not self.disabled_state_visible:
            raise ValueError(
                "disabled_state_visible must remain true for canonical interaction surface entries."
            )

        if not self.forbidden_state_visible:
            raise ValueError(
                "forbidden_state_visible must remain true for canonical interaction surface entries."
            )

        if not self.audit_visible:
            raise ValueError(
                "audit_visible must remain true for canonical interaction surface entries."
            )

        if self.surface_class == "approval_bound_surface":
            if not self.approval_required:
                raise ValueError(
                    "approval_bound_surface entries must have approval_required=True."
                )
            if not self.pending_approval_visible:
                raise ValueError(
                    "approval_bound_surface entries must expose pending_approval_visible=True."
                )

        if self.surface_class == "read_only_surface":
            if self.approval_required:
                raise ValueError(
                    "read_only_surface entries must have approval_required=False."
                )


@dataclass(frozen=True, slots=True)
class MainOperatorInteractionSurfaceContract:
    """Canonical main-operator interaction surface contract."""

    contract_id: str
    total_entries: int
    read_only_surface_entries: int
    approval_bound_surface_entries: int
    pending_approval_visible_entries: int
    handoff_ready_entries: int
    audit_visible_entries: int
    operator_visible_entries: int
    entries: tuple[MainOperatorInteractionSurfaceEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical main-operator interaction surface contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.read_only_surface_entries != sum(
            1 for entry in self.entries if entry.surface_class == "read_only_surface"
        ):
            raise ValueError(
                "read_only_surface_entries must match read_only_surface count."
            )

        if self.approval_bound_surface_entries != sum(
            1
            for entry in self.entries
            if entry.surface_class == "approval_bound_surface"
        ):
            raise ValueError(
                "approval_bound_surface_entries must match approval_bound_surface count."
            )

        if self.pending_approval_visible_entries != sum(
            1 for entry in self.entries if entry.pending_approval_visible
        ):
            raise ValueError(
                "pending_approval_visible_entries must match pending_approval_visible count."
            )

        if self.handoff_ready_entries != sum(
            1 for entry in self.entries if entry.handoff_ready
        ):
            raise ValueError(
                "handoff_ready_entries must match handoff_ready count."
            )

        if self.audit_visible_entries != sum(
            1 for entry in self.entries if entry.audit_visible
        ):
            raise ValueError(
                "audit_visible_entries must match audit_visible count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
