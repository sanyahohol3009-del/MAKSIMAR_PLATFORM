from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_dashboard_screen_state_contract import (
    build_operator_dashboard_screen_state_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_renderer_contract import (
    build_visual_renderer_contract,
)


RenderHandoffState = Literal[
    "render_handoff_ready",
]

RenderHandoffClass = Literal[
    "main_operator_render_handoff",
]

ALL_RENDER_HANDOFF_STATES: tuple[RenderHandoffState, ...] = (
    "render_handoff_ready",
)

ALL_RENDER_HANDOFF_CLASSES: tuple[RenderHandoffClass, ...] = (
    "main_operator_render_handoff",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorDashboardRenderHandoffEntry:
    """Canonical operator dashboard render-handoff entry."""

    render_handoff_id: str
    dashboard_id: str
    render_surface_id: str
    render_handoff_state: RenderHandoffState
    render_handoff_class: RenderHandoffClass
    screen_state_ready: bool
    renderer_registered: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard render-handoff entry."""
        _require_non_empty(self.render_handoff_id, "render_handoff_id")
        _require_non_empty(self.dashboard_id, "dashboard_id")
        _require_non_empty(self.render_surface_id, "render_surface_id")
        _require_non_empty(self.description, "description")

        if self.render_handoff_state not in ALL_RENDER_HANDOFF_STATES:
            raise ValueError(
                "render_handoff_state must be one of "
                f"{ALL_RENDER_HANDOFF_STATES}, got {self.render_handoff_state!r}."
            )

        if self.render_handoff_class not in ALL_RENDER_HANDOFF_CLASSES:
            raise ValueError(
                "render_handoff_class must be one of "
                f"{ALL_RENDER_HANDOFF_CLASSES}, got {self.render_handoff_class!r}."
            )

        if not self.screen_state_ready:
            raise ValueError(
                "screen_state_ready must remain true for canonical render-handoff entries."
            )

        if not self.renderer_registered:
            raise ValueError(
                "renderer_registered must remain true for canonical render-handoff entries."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical render-handoff entries."
            )


@dataclass(frozen=True, slots=True)
class OperatorDashboardRenderHandoffContract:
    """Canonical operator dashboard render-handoff contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorDashboardRenderHandoffEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical operator dashboard render-handoff contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.render_handoff_state == "render_handoff_ready"
        ):
            raise ValueError(
                "ready_entries must match render_handoff_ready count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_dashboard_render_handoff_contract() -> OperatorDashboardRenderHandoffContract:
    """Build canonical operator dashboard render-handoff contract."""
    screen_state_contract = build_operator_dashboard_screen_state_contract()
    renderer_contract = build_visual_renderer_contract()

    screen_entry = screen_state_contract.entries[0]

    entries = (
        OperatorDashboardRenderHandoffEntry(
            render_handoff_id="operator_dashboard_render_handoff_001",
            dashboard_id=screen_entry.dashboard_id,
            render_surface_id="render_surface_workspace_operator_main_001",
            render_handoff_state="render_handoff_ready",
            render_handoff_class="main_operator_render_handoff",
            screen_state_ready=screen_entry.visible_state_ready,
            renderer_registered=renderer_contract.total_entries >= 1,
            operator_visible=True,
            description=(
                "Canonical operator dashboard render-handoff entry bridging "
                "screen state into the registered visual renderer surface."
            ),
        ),
    )

    return OperatorDashboardRenderHandoffContract(
        contract_id="operator_dashboard_render_handoff_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.render_handoff_state == "render_handoff_ready"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
