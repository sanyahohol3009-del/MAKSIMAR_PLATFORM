from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_canonical_panel_contract import (
    build_visual_shell_canonical_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualShellContract:
    shell_id: str
    canonical_panel_contract_id: str
    render_surface_contract_id: str
    theme_id: str
    shell_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.shell_id, "shell_id")
        _require_non_empty(self.canonical_panel_contract_id, "canonical_panel_contract_id")
        _require_non_empty(self.render_surface_contract_id, "render_surface_contract_id")
        _require_non_empty(self.theme_id, "theme_id")
        _require_non_empty(self.description, "description")

        if not self.shell_ready:
            raise ValueError(
                "shell_ready must remain true for canonical visual shell contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual shell contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual shell contract."
            )


def build_visual_shell_contract() -> VisualShellContract:
    canonical_panel_contract = build_visual_shell_canonical_panel_contract()
    render_surface_contract = build_visual_render_surface_contract()
    theme_contract = build_visual_theme_contract()

    return VisualShellContract(
        shell_id="visual_shell_contract_001",
        canonical_panel_contract_id=canonical_panel_contract.contract_id,
        render_surface_contract_id=render_surface_contract.contract_id,
        theme_id=theme_contract.theme_id,
        shell_ready=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual shell contract for HUD rendering foundation.",
    )
