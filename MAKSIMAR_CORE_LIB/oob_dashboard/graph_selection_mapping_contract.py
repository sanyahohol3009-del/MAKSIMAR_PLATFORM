from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.dataflow_graph_adapter_contract import (
    build_dataflow_graph_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_graph_adapter_contract import (
    build_dependency_graph_adapter_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GraphSelectionMappingEntry:
    selection_entry_id: str
    selection_scope: str
    canonical_selection_id: str
    projection_target_id: str
    selection_kind: str
    canonical_id_preserved: bool
    vendor_selection_exposed: bool
    selection_mapping_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.selection_entry_id, "selection_entry_id")
        _require_non_empty(self.selection_scope, "selection_scope")
        _require_non_empty(self.canonical_selection_id, "canonical_selection_id")
        _require_non_empty(self.projection_target_id, "projection_target_id")
        _require_non_empty(self.selection_kind, "selection_kind")
        _require_non_empty(self.description, "description")

        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical graph selection mapping entries."
            )
        if self.vendor_selection_exposed:
            raise ValueError(
                "vendor_selection_exposed must remain false for canonical graph selection mapping entries."
            )
        if not self.selection_mapping_ready:
            raise ValueError(
                "selection_mapping_ready must remain true for canonical graph selection mapping entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical graph selection mapping entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical graph selection mapping entries."
            )


@dataclass(frozen=True, slots=True)
class GraphSelectionMappingContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    selection_mapping_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[GraphSelectionMappingEntry, ...]

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
        if self.selection_mapping_ready_entries != sum(
            1 for entry in self.entries if entry.selection_mapping_ready
        ):
            raise ValueError(
                "selection_mapping_ready_entries must match selection_mapping_ready count."
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


def build_graph_selection_mapping_contract() -> GraphSelectionMappingContract:
    dependency_adapter = build_dependency_graph_adapter_contract()
    dataflow_adapter = build_dataflow_graph_adapter_contract()

    entries = (
        GraphSelectionMappingEntry(
            selection_entry_id="graph_selection_mapping_001",
            selection_scope="dependency_graph_selection",
            canonical_selection_id="dependency_graph_primary_selection",
            projection_target_id=dependency_adapter.entries[0].graph_projection_id,
            selection_kind="dependency_projection",
            canonical_id_preserved=True,
            vendor_selection_exposed=False,
            selection_mapping_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical graph selection mapping for dependency graph primary selection.",
        ),
        GraphSelectionMappingEntry(
            selection_entry_id="graph_selection_mapping_002",
            selection_scope="dataflow_graph_selection",
            canonical_selection_id="dataflow_graph_primary_selection",
            projection_target_id=dataflow_adapter.entries[0].graph_projection_id,
            selection_kind="dataflow_projection",
            canonical_id_preserved=True,
            vendor_selection_exposed=False,
            selection_mapping_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical graph selection mapping for dataflow graph primary selection.",
        ),
        GraphSelectionMappingEntry(
            selection_entry_id="graph_selection_mapping_003",
            selection_scope="combined_graph_inspect_selection",
            canonical_selection_id="combined_graph_inspect_selection",
            projection_target_id=dependency_adapter.entries[-1].graph_projection_id,
            selection_kind="inspect_projection",
            canonical_id_preserved=True,
            vendor_selection_exposed=False,
            selection_mapping_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical graph selection mapping for combined graph inspect selection.",
        ),
    )

    return GraphSelectionMappingContract(
        contract_id="graph_selection_mapping_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        selection_mapping_ready_entries=sum(
            1 for entry in entries if entry.selection_mapping_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
