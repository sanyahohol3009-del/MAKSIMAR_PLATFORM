from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualStatusBarContract:
    status_bar_id: str
    theme_id: str
    global_health_visible: bool
    workspace_state_visible: bool
    mode_visible: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.status_bar_id, "status_bar_id")
        _require_non_empty(self.theme_id, "theme_id")
        _require_non_empty(self.description, "description")

        if not self.global_health_visible:
            raise ValueError(
                "global_health_visible must remain true for canonical visual status bar contract."
            )
        if not self.workspace_state_visible:
            raise ValueError(
                "workspace_state_visible must remain true for canonical visual status bar contract."
            )
        if not self.mode_visible:
            raise ValueError(
                "mode_visible must remain true for canonical visual status bar contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual status bar contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual status bar contract."
            )


def build_visual_status_bar_contract() -> VisualStatusBarContract:
    theme_contract = build_visual_theme_contract()

    return VisualStatusBarContract(
        status_bar_id="visual_status_bar_contract_001",
        theme_id=theme_contract.theme_id,
        global_health_visible=True,
        workspace_state_visible=True,
        mode_visible=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual status bar contract.",
    )
