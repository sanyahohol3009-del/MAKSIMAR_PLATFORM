from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.data_flow_panel_contract import (
    build_data_flow_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    build_graph_render_adapter_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DataflowGraphAdapterEntry:
    adapter_entry_id: str
    dataflow_panel_id: str
    graph_adapter_contract_id: str
    canonical_flow_id: str
    source_component: str
    target_component: str
    flow_class: str
    graph_projection_id: str
    canonical_id_preserved: bool
    vendor_flow_id_exposed: bool
    flow_projection_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.dataflow_panel_id, "dataflow_panel_id")
        _require_non_empty(self.graph_adapter_contract_id, "graph_adapter_contract_id")
        _require_non_empty(self.canonical_flow_id, "canonical_flow_id")
        _require_non_empty(self.source_component, "source_component")
        _require_non_empty(self.target_component, "target_component")
        _require_non_empty(self.flow_class, "flow_class")
        _require_non_empty(self.graph_projection_id, "graph_projection_id")
        _require_non_empty(self.description, "description")

        if self.source_component == self.target_component:
            raise ValueError("source_component and target_component must differ.")
        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical dataflow graph adapter entries."
            )
        if self.vendor_flow_id_exposed:
            raise ValueError(
                "vendor_flow_id_exposed must remain false for canonical dataflow graph adapter entries."
            )
        if not self.flow_projection_ready:
            raise ValueError(
                "flow_projection_ready must remain true for canonical dataflow graph adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical dataflow graph adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical dataflow graph adapter entries."
            )


@dataclass(frozen=True, slots=True)
class DataflowGraphAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    flow_projection_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[DataflowGraphAdapterEntry, ...]

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
        if self.flow_projection_ready_entries != sum(
            1 for entry in self.entries if entry.flow_projection_ready
        ):
            raise ValueError(
                "flow_projection_ready_entries must match flow_projection_ready count."
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


def build_dataflow_graph_adapter_contract() -> DataflowGraphAdapterContract:
    dataflow_panel = build_data_flow_panel_contract()
    graph_adapter = build_graph_render_adapter_contract()

    entries = tuple(
        DataflowGraphAdapterEntry(
            adapter_entry_id=f"dataflow_graph_adapter_{index:03d}",
            dataflow_panel_id=dataflow_panel.panel_id,
            graph_adapter_contract_id=graph_adapter.contract_id,
            canonical_flow_id=f"{entry.source_component}_to_{entry.target_component}_flow",
            source_component=entry.source_component,
            target_component=entry.target_component,
            flow_class=entry.flow_class,
            graph_projection_id=f"{entry.source_component}_to_{entry.target_component}_flow_projection",
            canonical_id_preserved=True,
            vendor_flow_id_exposed=False,
            flow_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=(
                f"Canonical dataflow graph adapter entry for "
                f"{entry.source_component} -> {entry.target_component}."
            ),
        )
        for index, entry in enumerate(dataflow_panel.entries, start=1)
    )

    return DataflowGraphAdapterContract(
        contract_id="dataflow_graph_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        flow_projection_ready_entries=sum(
            1 for entry in entries if entry.flow_projection_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
