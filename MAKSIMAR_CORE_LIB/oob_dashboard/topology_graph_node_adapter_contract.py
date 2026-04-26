from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    build_graph_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.node_topology_panel_contract import (
    build_node_topology_panel_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class TopologyGraphNodeAdapterEntry:
    adapter_entry_id: str
    topology_panel_id: str
    graph_adapter_contract_id: str
    canonical_node_id: str
    node_role_type: str
    graph_projection_id: str
    canonical_id_preserved: bool
    vendor_node_id_exposed: bool
    node_projection_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.topology_panel_id, "topology_panel_id")
        _require_non_empty(self.graph_adapter_contract_id, "graph_adapter_contract_id")
        _require_non_empty(self.canonical_node_id, "canonical_node_id")
        _require_non_empty(self.node_role_type, "node_role_type")
        _require_non_empty(self.graph_projection_id, "graph_projection_id")
        _require_non_empty(self.description, "description")

        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical topology graph node adapter entries."
            )
        if self.vendor_node_id_exposed:
            raise ValueError(
                "vendor_node_id_exposed must remain false for canonical topology graph node adapter entries."
            )
        if not self.node_projection_ready:
            raise ValueError(
                "node_projection_ready must remain true for canonical topology graph node adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical topology graph node adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical topology graph node adapter entries."
            )


@dataclass(frozen=True, slots=True)
class TopologyGraphNodeAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    node_projection_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[TopologyGraphNodeAdapterEntry, ...]

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
        if self.node_projection_ready_entries != sum(
            1 for entry in self.entries if entry.node_projection_ready
        ):
            raise ValueError(
                "node_projection_ready_entries must match node_projection_ready count."
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


def build_topology_graph_node_adapter_contract() -> TopologyGraphNodeAdapterContract:
    topology_panel = build_node_topology_panel_contract()
    graph_adapter = build_graph_render_adapter_contract()

    entries = tuple(
        TopologyGraphNodeAdapterEntry(
            adapter_entry_id=f"topology_graph_node_adapter_{index:03d}",
            topology_panel_id=topology_panel.panel_id,
            graph_adapter_contract_id=graph_adapter.contract_id,
            canonical_node_id=entry.node_id,
            node_role_type=entry.role_type,
            graph_projection_id=f"{entry.node_id}_graph_projection",
            canonical_id_preserved=True,
            vendor_node_id_exposed=False,
            node_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical topology graph node adapter entry for {entry.node_id}.",
        )
        for index, entry in enumerate(topology_panel.entries, start=1)
    )

    return TopologyGraphNodeAdapterContract(
        contract_id="topology_graph_node_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        node_projection_ready_entries=sum(
            1 for entry in entries if entry.node_projection_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
