from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_contract import (
    build_visual_backend_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualChartBackendContract:
    contract_id: str
    backend_id: str
    chart_backend_name: str
    supports_line_series: bool
    supports_status_series: bool
    supports_multi_series: bool
    supports_responsive_rendering: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.chart_backend_name, "chart_backend_name")
        _require_non_empty(self.description, "description")

        if not self.supports_line_series:
            raise ValueError(
                "supports_line_series must remain true for canonical visual chart backend contract."
            )
        if not self.supports_status_series:
            raise ValueError(
                "supports_status_series must remain true for canonical visual chart backend contract."
            )
        if not self.supports_multi_series:
            raise ValueError(
                "supports_multi_series must remain true for canonical visual chart backend contract."
            )
        if not self.supports_responsive_rendering:
            raise ValueError(
                "supports_responsive_rendering must remain true for canonical visual chart backend contract."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical visual chart backend contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual chart backend contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual chart backend contract."
            )


def build_visual_chart_backend_contract() -> VisualChartBackendContract:
    backend_contract = build_visual_backend_contract()
    chart_entry = next(
        entry for entry in backend_contract.entries if entry.backend_type == "chart_backend"
    )

    return VisualChartBackendContract(
        contract_id="visual_chart_backend_contract_001",
        backend_id=chart_entry.backend_id,
        chart_backend_name=chart_entry.backend_name,
        supports_line_series=True,
        supports_status_series=True,
        supports_multi_series=True,
        supports_responsive_rendering=True,
        replaceable=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual chart backend boundary contract.",
    )
