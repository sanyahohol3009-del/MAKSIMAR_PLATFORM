from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    build_graph_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_dashboard_surface_contract import (
    build_module_dashboard_surface_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleGraphSurfaceAdapterEntry:
    adapter_entry_id: str
    module_id: str
    surface_id: str
    workspace_id: str
    graph_adapter_contract_id: str
    graph_projection_id: str
    canonical_id_preserved: bool
    vendor_surface_id_exposed: bool
    surface_projection_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.surface_id, "surface_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.graph_adapter_contract_id, "graph_adapter_contract_id")
        _require_non_empty(self.graph_projection_id, "graph_projection_id")
        _require_non_empty(self.description, "description")

        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical module graph surface adapter entries."
            )
        if self.vendor_surface_id_exposed:
            raise ValueError(
                "vendor_surface_id_exposed must remain false for canonical module graph surface adapter entries."
            )
        if not self.surface_projection_ready:
            raise ValueError(
                "surface_projection_ready must remain true for canonical module graph surface adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module graph surface adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module graph surface adapter entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleGraphSurfaceAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    surface_projection_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[ModuleGraphSurfaceAdapterEntry, ...]

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
        if self.surface_projection_ready_entries != sum(
            1 for entry in self.entries if entry.surface_projection_ready
        ):
            raise ValueError(
                "surface_projection_ready_entries must match surface_projection_ready count."
            )
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


def build_module_graph_surface_adapter_contract() -> ModuleGraphSurfaceAdapterContract:
    surface_contract = build_module_dashboard_surface_contract()
    graph_adapter = build_graph_render_adapter_contract()

    entries = tuple(
        ModuleGraphSurfaceAdapterEntry(
            adapter_entry_id=f"module_graph_surface_adapter_{index:03d}",
            module_id=entry.module_id,
            surface_id=entry.surface_id,
            workspace_id=entry.workspace_id,
            graph_adapter_contract_id=graph_adapter.contract_id,
            graph_projection_id=f"{entry.module_id}_surface_graph_projection",
            canonical_id_preserved=True,
            vendor_surface_id_exposed=False,
            surface_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical module graph surface adapter entry for {entry.module_id}.",
        )
        for index, entry in enumerate(surface_contract.entries, start=1)
    )

    return ModuleGraphSurfaceAdapterContract(
        contract_id="module_graph_surface_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        surface_projection_ready_entries=sum(
            1 for entry in entries if entry.surface_projection_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
