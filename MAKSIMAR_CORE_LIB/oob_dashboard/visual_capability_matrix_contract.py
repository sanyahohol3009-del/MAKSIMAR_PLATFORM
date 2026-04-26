from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_contract import (
    build_visual_backend_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_replaceability_contract import (
    build_visual_backend_replaceability_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_chart_backend_contract import (
    build_visual_chart_backend_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_graph_backend_contract import (
    build_visual_graph_backend_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_overlay_backend_contract import (
    build_visual_overlay_backend_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualCapabilityMatrixEntry:
    capability_entry_id: str
    backend_id: str
    capability_scope: str
    graph_capable: bool
    chart_capable: bool
    overlay_capable: bool
    motion_capable: bool
    degraded_fallback_supported: bool
    swap_safe: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.capability_entry_id, "capability_entry_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.capability_scope, "capability_scope")
        _require_non_empty(self.description, "description")

        if not any(
            (
                self.graph_capable,
                self.chart_capable,
                self.overlay_capable,
                self.motion_capable,
            )
        ):
            raise ValueError(
                "At least one capability flag must remain true for canonical visual capability matrix entries."
            )
        if not self.degraded_fallback_supported:
            raise ValueError(
                "degraded_fallback_supported must remain true for canonical visual capability matrix entries."
            )
        if not self.swap_safe:
            raise ValueError(
                "swap_safe must remain true for canonical visual capability matrix entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual capability matrix entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual capability matrix entries."
            )


@dataclass(frozen=True, slots=True)
class VisualCapabilityMatrixContract:
    contract_id: str
    total_entries: int
    degraded_fallback_supported_entries: int
    swap_safe_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualCapabilityMatrixEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.degraded_fallback_supported_entries != sum(
            1 for entry in self.entries if entry.degraded_fallback_supported
        ):
            raise ValueError(
                "degraded_fallback_supported_entries must match degraded_fallback_supported count."
            )
        if self.swap_safe_entries != sum(
            1 for entry in self.entries if entry.swap_safe
        ):
            raise ValueError("swap_safe_entries must match swap_safe count.")
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


def build_visual_capability_matrix_contract() -> VisualCapabilityMatrixContract:
    backend_contract = build_visual_backend_contract()
    graph_backend = build_visual_graph_backend_contract()
    chart_backend = build_visual_chart_backend_contract()
    overlay_backend = build_visual_overlay_backend_contract()
    replaceability_contract = build_visual_backend_replaceability_contract()

    replaceable_backend_ids = {entry.backend_id for entry in replaceability_contract.entries}

    entries = (
        VisualCapabilityMatrixEntry(
            capability_entry_id="visual_capability_matrix_001",
            backend_id=backend_contract.entries[0].backend_id,
            capability_scope=graph_backend.graph_backend_name,
            graph_capable=True,
            chart_capable=False,
            overlay_capable=False,
            motion_capable=False,
            degraded_fallback_supported=True,
            swap_safe=backend_contract.entries[0].backend_id in replaceable_backend_ids,
            operator_visible=True,
            truth_bound=True,
            description="Canonical capability matrix entry for graph backend.",
        ),
        VisualCapabilityMatrixEntry(
            capability_entry_id="visual_capability_matrix_002",
            backend_id=backend_contract.entries[1].backend_id,
            capability_scope=chart_backend.chart_backend_name,
            graph_capable=False,
            chart_capable=True,
            overlay_capable=False,
            motion_capable=False,
            degraded_fallback_supported=True,
            swap_safe=backend_contract.entries[1].backend_id in replaceable_backend_ids,
            operator_visible=True,
            truth_bound=True,
            description="Canonical capability matrix entry for chart backend.",
        ),
        VisualCapabilityMatrixEntry(
            capability_entry_id="visual_capability_matrix_003",
            backend_id=backend_contract.entries[2].backend_id,
            capability_scope=overlay_backend.overlay_backend_name,
            graph_capable=False,
            chart_capable=False,
            overlay_capable=True,
            motion_capable=False,
            degraded_fallback_supported=True,
            swap_safe=backend_contract.entries[2].backend_id in replaceable_backend_ids,
            operator_visible=True,
            truth_bound=True,
            description="Canonical capability matrix entry for overlay backend.",
        ),
        VisualCapabilityMatrixEntry(
            capability_entry_id="visual_capability_matrix_004",
            backend_id="motion_backend_virtual_001",
            capability_scope="motion_render_adapter_boundary",
            graph_capable=False,
            chart_capable=False,
            overlay_capable=False,
            motion_capable=True,
            degraded_fallback_supported=True,
            swap_safe="motion_backend_virtual_001" in replaceable_backend_ids,
            operator_visible=True,
            truth_bound=True,
            description="Canonical capability matrix entry for motion backend boundary.",
        ),
    )

    return VisualCapabilityMatrixContract(
        contract_id="visual_capability_matrix_contract_001",
        total_entries=len(entries),
        degraded_fallback_supported_entries=sum(
            1 for entry in entries if entry.degraded_fallback_supported
        ),
        swap_safe_entries=sum(1 for entry in entries if entry.swap_safe),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
