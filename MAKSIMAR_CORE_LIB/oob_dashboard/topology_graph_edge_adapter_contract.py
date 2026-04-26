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
class TopologyGraphEdgeAdapterEntry:
    adapter_entry_id: str
    topology_panel_id: str
    graph_adapter_contract_id: str
    canonical_edge_id: str
    source_node_id: str
    target_node_id: str
    edge_class: str
    graph_projection_id: str
    canonical_id_preserved: bool
    vendor_edge_id_exposed: bool
    edge_projection_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.topology_panel_id, "topology_panel_id")
        _require_non_empty(self.graph_adapter_contract_id, "graph_adapter_contract_id")
        _require_non_empty(self.canonical_edge_id, "canonical_edge_id")
        _require_non_empty(self.source_node_id, "source_node_id")
        _require_non_empty(self.target_node_id, "target_node_id")
        _require_non_empty(self.edge_class, "edge_class")
        _require_non_empty(self.graph_projection_id, "graph_projection_id")
        _require_non_empty(self.description, "description")

        if self.source_node_id == self.target_node_id:
            raise ValueError("source_node_id and target_node_id must differ.")
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical topology graph edge adapter entries."
            )
        if self.vendor_edge_id_exposed:
            raise ValueError(
                "vendor_edge_id_exposed must remain false for canonical topology graph edge adapter entries."
            )
        if not self.edge_projection_ready:
            raise ValueError(
                "edge_projection_ready must remain true for canonical topology graph edge adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical topology graph edge adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical topology graph edge adapter entries."
            )


@dataclass(frozen=True, slots=True)
class TopologyGraphEdgeAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    edge_projection_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[TopologyGraphEdgeAdapterEntry, ...]

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
        if self.edge_projection_ready_entries != sum(
            1 for entry in self.entries if entry.edge_projection_ready
        ):
            raise ValueError(
                "edge_projection_ready_entries must match edge_projection_ready count."
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


def build_topology_graph_edge_adapter_contract() -> TopologyGraphEdgeAdapterContract:
    topology_panel = build_node_topology_panel_contract()
    graph_adapter = build_graph_render_adapter_contract()

    anchor_node = topology_panel.entries[0]
    downstream_nodes = topology_panel.entries[1:]

    entries = tuple(
        TopologyGraphEdgeAdapterEntry(
            adapter_entry_id=f"topology_graph_edge_adapter_{index:03d}",
            topology_panel_id=topology_panel.panel_id,
            graph_adapter_contract_id=graph_adapter.contract_id,
            canonical_edge_id=f"{entry.node_id}_to_{anchor_node.node_id}_edge",
            source_node_id=entry.node_id,
            target_node_id=anchor_node.node_id,
            edge_class="topology_anchor_edge",
            graph_projection_id=f"{entry.node_id}_to_{anchor_node.node_id}_graph_edge",
            canonical_id_preserved=True,
            vendor_edge_id_exposed=False,
            edge_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical topology graph edge adapter entry for {entry.node_id} -> {anchor_node.node_id}.",
        )
        for index, entry in enumerate(downstream_nodes, start=1)
    )

    return TopologyGraphEdgeAdapterContract(
        contract_id="topology_graph_edge_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        edge_projection_ready_entries=sum(
            1 for entry in entries if entry.edge_projection_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
