from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualBottomTickerContract:
    bottom_ticker_id: str
    theme_id: str
    ticker_enabled: bool
    incident_summary_visible: bool
    flow_state_visible: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.bottom_ticker_id, "bottom_ticker_id")
        _require_non_empty(self.theme_id, "theme_id")
        _require_non_empty(self.description, "description")

        if not self.ticker_enabled:
            raise ValueError(
                "ticker_enabled must remain true for canonical visual bottom ticker contract."
            )
        if not self.incident_summary_visible:
            raise ValueError(
                "incident_summary_visible must remain true for canonical visual bottom ticker contract."
            )
        if not self.flow_state_visible:
            raise ValueError(
                "flow_state_visible must remain true for canonical visual bottom ticker contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual bottom ticker contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual bottom ticker contract."
            )


def build_visual_bottom_ticker_contract() -> VisualBottomTickerContract:
    theme_contract = build_visual_theme_contract()

    return VisualBottomTickerContract(
        bottom_ticker_id="visual_bottom_ticker_contract_001",
        theme_id=theme_contract.theme_id,
        ticker_enabled=True,
        incident_summary_visible=True,
        flow_state_visible=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual bottom ticker contract.",
    )
