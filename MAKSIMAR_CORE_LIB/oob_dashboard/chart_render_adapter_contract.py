from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_chart_backend_contract import (
    build_visual_chart_backend_contract,
)

ChartAdapterMode = Literal[
    "canonical_to_chart_backend",
]

_ALLOWED_CHART_ADAPTER_MODES: tuple[ChartAdapterMode, ...] = (
    "canonical_to_chart_backend",
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ChartRenderAdapterEntry:
    adapter_entry_id: str
    backend_id: str
    adapter_target: str
    adapter_mode: ChartAdapterMode
    canonical_id_preserved: bool
    vendor_series_exposed: bool
    truth_leakage_allowed: bool
    replaceable: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.adapter_target, "adapter_target")
        _require_non_empty(self.description, "description")

        if self.adapter_mode not in _ALLOWED_CHART_ADAPTER_MODES:
            raise ValueError(
                f"adapter_mode must be one of {_ALLOWED_CHART_ADAPTER_MODES}, got {self.adapter_mode!r}."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical chart render adapter entries."
            )
        if self.vendor_series_exposed:
            raise ValueError(
                "vendor_series_exposed must remain false for canonical chart render adapter entries."
            )
        if self.truth_leakage_allowed:
            raise ValueError(
                "truth_leakage_allowed must remain false for canonical chart render adapter entries."
            )
        if not self.replaceable:
            raise ValueError(
                "replaceable must remain true for canonical chart render adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical chart render adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical chart render adapter entries."
            )


@dataclass(frozen=True, slots=True)
class ChartRenderAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[ChartRenderAdapterEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.canonical_id_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_id_preserved
        ):
            raise ValueError(
                "canonical_id_preserved_entries must match canonical_id_preserved count."
            )
        if self.replaceable_entries != sum(
            1 for entry in self.entries if entry.replaceable
        ):
            raise ValueError("replaceable_entries must match replaceable count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_chart_render_adapter_contract() -> ChartRenderAdapterContract:
    chart_backend = build_visual_chart_backend_contract()

    entries = (
        ChartRenderAdapterEntry(
            adapter_entry_id="chart_render_adapter_001",
            backend_id=chart_backend.backend_id,
            adapter_target="node_resources_chart_projection",
            adapter_mode="canonical_to_chart_backend",
            canonical_id_preserved=True,
            vendor_series_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical chart adapter entry for node resources projection.",
        ),
        ChartRenderAdapterEntry(
            adapter_entry_id="chart_render_adapter_002",
            backend_id=chart_backend.backend_id,
            adapter_target="export_validation_assets_chart_projection",
            adapter_mode="canonical_to_chart_backend",
            canonical_id_preserved=True,
            vendor_series_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical chart adapter entry for export/validation/assets projection.",
        ),
        ChartRenderAdapterEntry(
            adapter_entry_id="chart_render_adapter_003",
            backend_id=chart_backend.backend_id,
            adapter_target="security_telemetry_chart_projection",
            adapter_mode="canonical_to_chart_backend",
            canonical_id_preserved=True,
            vendor_series_exposed=False,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical chart adapter entry for security/telemetry projection.",
        ),
    )

    return ChartRenderAdapterContract(
        contract_id="chart_render_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        replaceable_entries=sum(1 for entry in entries if entry.replaceable),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
