from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_map_panel_contract import (
    build_dependency_map_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    build_graph_render_adapter_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DependencyGraphAdapterEntry:
    adapter_entry_id: str
    dependency_panel_id: str
    graph_adapter_contract_id: str
    canonical_dependency_id: str
    upstream_module_id: str
    downstream_module_id: str
    dependency_kind: str
    graph_projection_id: str
    canonical_id_preserved: bool
    vendor_dependency_id_exposed: bool
    dependency_projection_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.dependency_panel_id, "dependency_panel_id")
        _require_non_empty(self.graph_adapter_contract_id, "graph_adapter_contract_id")
        _require_non_empty(self.canonical_dependency_id, "canonical_dependency_id")
        _require_non_empty(self.upstream_module_id, "upstream_module_id")
        _require_non_empty(self.downstream_module_id, "downstream_module_id")
        _require_non_empty(self.dependency_kind, "dependency_kind")
        _require_non_empty(self.graph_projection_id, "graph_projection_id")
        _require_non_empty(self.description, "description")

        if self.upstream_module_id == self.downstream_module_id:
            raise ValueError("upstream_module_id and downstream_module_id must differ.")
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical dependency graph adapter entries."
            )
        if self.vendor_dependency_id_exposed:
            raise ValueError(
                "vendor_dependency_id_exposed must remain false for canonical dependency graph adapter entries."
            )
        if not self.dependency_projection_ready:
            raise ValueError(
                "dependency_projection_ready must remain true for canonical dependency graph adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical dependency graph adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical dependency graph adapter entries."
            )


@dataclass(frozen=True, slots=True)
class DependencyGraphAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    dependency_projection_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[DependencyGraphAdapterEntry, ...]

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
        if self.dependency_projection_ready_entries != sum(
            1 for entry in self.entries if entry.dependency_projection_ready
        ):
            raise ValueError(
                "dependency_projection_ready_entries must match dependency_projection_ready count."
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


def build_dependency_graph_adapter_contract() -> DependencyGraphAdapterContract:
    dependency_panel = build_dependency_map_panel_contract()
    graph_adapter = build_graph_render_adapter_contract()

    entries = tuple(
        DependencyGraphAdapterEntry(
            adapter_entry_id=f"dependency_graph_adapter_{index:03d}",
            dependency_panel_id=dependency_panel.panel_id,
            graph_adapter_contract_id=graph_adapter.contract_id,
            canonical_dependency_id=f"{entry.upstream_module_id}_to_{entry.downstream_module_id}_dependency",
            upstream_module_id=entry.upstream_module_id,
            downstream_module_id=entry.downstream_module_id,
            dependency_kind=entry.dependency_kind,
            graph_projection_id=f"{entry.upstream_module_id}_to_{entry.downstream_module_id}_dependency_projection",
            canonical_id_preserved=True,
            vendor_dependency_id_exposed=False,
            dependency_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=(
                f"Canonical dependency graph adapter entry for "
                f"{entry.upstream_module_id} -> {entry.downstream_module_id}."
            ),
        )
        for index, entry in enumerate(dependency_panel.entries, start=1)
    )

    return DependencyGraphAdapterContract(
        contract_id="dependency_graph_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        dependency_projection_ready_entries=sum(
            1 for entry in entries if entry.dependency_projection_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
