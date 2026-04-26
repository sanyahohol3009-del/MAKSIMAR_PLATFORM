from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SandboxRouteState = Literal[
    "sandbox_route_ready",
]

SandboxRouteClass = Literal[
    "read_only_sandbox_route",
    "approval_bound_sandbox_route",
]

SandboxRouteMode = Literal[
    "preview_review_simulation_replay_sandbox_route",
    "preview_review_approval_simulation_replay_sandbox_route",
]

ALL_SANDBOX_ROUTE_STATES: tuple[SandboxRouteState, ...] = (
    "sandbox_route_ready",
)

ALL_SANDBOX_ROUTE_CLASSES: tuple[SandboxRouteClass, ...] = (
    "read_only_sandbox_route",
    "approval_bound_sandbox_route",
)

ALL_SANDBOX_ROUTE_MODES: tuple[SandboxRouteMode, ...] = (
    "preview_review_simulation_replay_sandbox_route",
    "preview_review_approval_simulation_replay_sandbox_route",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class SandboxRouteEntry:
    """Canonical sandbox route entry."""

    sandbox_route_id: str
    operator_intent_id: str
    panel_id: str
    workspace_id: str
    sandbox_route_state: SandboxRouteState
    sandbox_route_class: SandboxRouteClass
    sandbox_route_mode: SandboxRouteMode
    approval_required: bool
    handoff_ready: bool
    sandbox_visible: bool
    operator_visible: bool
    trace_id: str
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.sandbox_route_id, "sandbox_route_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.trace_id, "trace_id")
        _require_non_empty(self.description, "description")

        if self.sandbox_route_state not in ALL_SANDBOX_ROUTE_STATES:
            raise ValueError(
                "sandbox_route_state must be one of "
                f"{ALL_SANDBOX_ROUTE_STATES}, got {self.sandbox_route_state!r}."
            )

        if self.sandbox_route_class not in ALL_SANDBOX_ROUTE_CLASSES:
            raise ValueError(
                "sandbox_route_class must be one of "
                f"{ALL_SANDBOX_ROUTE_CLASSES}, got {self.sandbox_route_class!r}."
            )

        if self.sandbox_route_mode not in ALL_SANDBOX_ROUTE_MODES:
            raise ValueError(
                "sandbox_route_mode must be one of "
                f"{ALL_SANDBOX_ROUTE_MODES}, got {self.sandbox_route_mode!r}."
            )

        if not self.handoff_ready:
            raise ValueError(
                "handoff_ready must remain true for canonical sandbox routes."
            )

        if not self.sandbox_visible:
            raise ValueError(
                "sandbox_visible must remain true for canonical sandbox routes."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical sandbox routes."
            )

        if (
            self.sandbox_route_class == "approval_bound_sandbox_route"
            and not self.approval_required
        ):
            raise ValueError(
                "approval_bound_sandbox_route must have approval_required=True."
            )

        if (
            self.sandbox_route_class == "read_only_sandbox_route"
            and self.approval_required
        ):
            raise ValueError(
                "read_only_sandbox_route must have approval_required=False."
            )

        if (
            self.sandbox_route_class == "approval_bound_sandbox_route"
            and self.sandbox_route_mode
            != "preview_review_approval_simulation_replay_sandbox_route"
        ):
            raise ValueError(
                "approval_bound_sandbox_route must use preview_review_approval_simulation_replay_sandbox_route."
            )

        if (
            self.sandbox_route_class == "read_only_sandbox_route"
            and self.sandbox_route_mode
            != "preview_review_simulation_replay_sandbox_route"
        ):
            raise ValueError(
                "read_only_sandbox_route must use preview_review_simulation_replay_sandbox_route."
            )


@dataclass(frozen=True, slots=True)
class SandboxRouteContract:
    """Canonical sandbox route contract."""

    contract_id: str
    total_entries: int
    read_only_sandbox_entries: int
    approval_bound_sandbox_entries: int
    sandbox_visible_entries: int
    operator_visible_entries: int
    entries: tuple[SandboxRouteEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.read_only_sandbox_entries != sum(
            1
            for entry in self.entries
            if entry.sandbox_route_class == "read_only_sandbox_route"
        ):
            raise ValueError(
                "read_only_sandbox_entries must match read_only_sandbox_route count."
            )

        if self.approval_bound_sandbox_entries != sum(
            1
            for entry in self.entries
            if entry.sandbox_route_class == "approval_bound_sandbox_route"
        ):
            raise ValueError(
                "approval_bound_sandbox_entries must match approval_bound_sandbox_route count."
            )

        if self.sandbox_visible_entries != sum(
            1 for entry in self.entries if entry.sandbox_visible
        ):
            raise ValueError(
                "sandbox_visible_entries must match sandbox_visible count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
