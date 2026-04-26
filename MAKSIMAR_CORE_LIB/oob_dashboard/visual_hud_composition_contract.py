from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_bottom_ticker_contract import (
    build_visual_bottom_ticker_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_explainability_sidebar_contract import (
    build_visual_explainability_sidebar_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_renderer_contract import (
    build_visual_renderer_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_contract import (
    build_visual_shell_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_signal_overlay_contract import (
    build_visual_signal_overlay_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_bar_contract import (
    build_visual_status_bar_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_topology_overlay_contract import (
    build_visual_topology_overlay_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualHudCompositionContract:
    composition_id: str
    shell_id: str
    renderer_id: str
    signal_overlay_ready: bool
    topology_overlay_ready: bool
    explainability_sidebar_ready: bool
    status_bar_ready: bool
    bottom_ticker_ready: bool
    composition_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.composition_id, "composition_id")
        _require_non_empty(self.shell_id, "shell_id")
        _require_non_empty(self.renderer_id, "renderer_id")
        _require_non_empty(self.description, "description")

        if not self.signal_overlay_ready:
            raise ValueError(
                "signal_overlay_ready must remain true for canonical visual HUD composition contract."
            )
        if not self.topology_overlay_ready:
            raise ValueError(
                "topology_overlay_ready must remain true for canonical visual HUD composition contract."
            )
        if not self.explainability_sidebar_ready:
            raise ValueError(
                "explainability_sidebar_ready must remain true for canonical visual HUD composition contract."
            )
        if not self.status_bar_ready:
            raise ValueError(
                "status_bar_ready must remain true for canonical visual HUD composition contract."
            )
        if not self.bottom_ticker_ready:
            raise ValueError(
                "bottom_ticker_ready must remain true for canonical visual HUD composition contract."
            )
        if not self.composition_ready:
            raise ValueError(
                "composition_ready must remain true for canonical visual HUD composition contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual HUD composition contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual HUD composition contract."
            )


def build_visual_hud_composition_contract() -> VisualHudCompositionContract:
    shell_contract = build_visual_shell_contract()
    renderer_contract = build_visual_renderer_contract()
    signal_overlay_contract = build_visual_signal_overlay_contract()
    topology_overlay_contract = build_visual_topology_overlay_contract()
    explainability_sidebar_contract = build_visual_explainability_sidebar_contract()
    status_bar_contract = build_visual_status_bar_contract()
    bottom_ticker_contract = build_visual_bottom_ticker_contract()

    return VisualHudCompositionContract(
        composition_id="visual_hud_composition_contract_001",
        shell_id=shell_contract.shell_id,
        renderer_id=renderer_contract.renderer_id,
        signal_overlay_ready=bool(signal_overlay_contract.entries),
        topology_overlay_ready=bool(topology_overlay_contract.entries),
        explainability_sidebar_ready=bool(explainability_sidebar_contract.entries),
        status_bar_ready=bool(status_bar_contract.status_bar_id),
        bottom_ticker_ready=bool(bottom_ticker_contract.bottom_ticker_id),
        composition_ready=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual HUD composition contract.",
    )
