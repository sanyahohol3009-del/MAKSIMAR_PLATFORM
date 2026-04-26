from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_edge_adapter_contract import (
    build_topology_graph_edge_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_node_adapter_contract import (
    build_topology_graph_node_adapter_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class TopologyGraphLayoutEntry:
    layout_entry_id: str
    canonical_node_id: str
    node_projection_id: str
    layout_zone: str
    x_slot: int
    y_slot: int
    layout_ready: bool
    canonical_id_preserved: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.layout_entry_id, "layout_entry_id")
        _require_non_empty(self.canonical_node_id, "canonical_node_id")
        _require_non_empty(self.node_projection_id, "node_projection_id")
        _require_non_empty(self.layout_zone, "layout_zone")
        _require_non_empty(self.description, "description")

        if self.x_slot < 0:
            raise ValueError("x_slot must be >= 0.")
        if self.y_slot < 0:
            raise ValueError("y_slot must be >= 0.")
        if not self.layout_ready:
            raise ValueError(
                "layout_ready must remain true for canonical topology graph layout entries."
            )
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical topology graph layout entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical topology graph layout entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical topology graph layout entries."
            )


@dataclass(frozen=True, slots=True)
class TopologyGraphLayoutContract:
    contract_id: str
    total_entries: int
    layout_ready_entries: int
    canonical_id_preserved_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    edge_count: int
    entries: Tuple[TopologyGraphLayoutEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.layout_ready_entries != sum(
            1 for entry in self.entries if entry.layout_ready
        ):
            raise ValueError("layout_ready_entries must match layout_ready count.")
        if self.canonical_id_preserved_entries != sum(
            1 for entry in self.entries if entry.canonical_id_preserved
        ):
            raise ValueError(
                "canonical_id_preserved_entries must match canonical_id_preserved count."
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
        if self.edge_count < 0:
            raise ValueError("edge_count must be >= 0.")


def build_topology_graph_layout_contract() -> TopologyGraphLayoutContract:
    node_adapter = build_topology_graph_node_adapter_contract()
    edge_adapter = build_topology_graph_edge_adapter_contract()

    slot_map = {
        "mobile_001": (1, 0),
        "dev_001": (0, 1),
        "home_001": (2, 1),
    }

    entries = tuple(
        TopologyGraphLayoutEntry(
            layout_entry_id=f"topology_graph_layout_{index:03d}",
            canonical_node_id=entry.canonical_node_id,
            node_projection_id=entry.graph_projection_id,
            layout_zone="topology_graph_main_zone",
            x_slot=slot_map[entry.canonical_node_id][0],
            y_slot=slot_map[entry.canonical_node_id][1],
            layout_ready=True,
            canonical_id_preserved=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical topology graph layout entry for {entry.canonical_node_id}.",
        )
        for index, entry in enumerate(node_adapter.entries, start=1)
    )

    return TopologyGraphLayoutContract(
        contract_id="topology_graph_layout_contract_001",
        total_entries=len(entries),
        layout_ready_entries=sum(1 for entry in entries if entry.layout_ready),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        edge_count=edge_adapter.total_entries,
        entries=entries,
    )
