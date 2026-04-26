from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    build_graph_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_navigation_entry_contract import (
    build_module_navigation_entry_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class ModuleGraphNavigationAdapterEntry:
    adapter_entry_id: str
    module_id: str
    navigation_id: str
    navigation_group: str
    graph_adapter_contract_id: str
    graph_projection_id: str
    canonical_id_preserved: bool
    vendor_navigation_id_exposed: bool
    navigation_projection_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.module_id, "module_id")
        _require_non_empty(self.navigation_id, "navigation_id")
        _require_non_empty(self.navigation_group, "navigation_group")
        _require_non_empty(self.graph_adapter_contract_id, "graph_adapter_contract_id")
        _require_non_empty(self.graph_projection_id, "graph_projection_id")
        _require_non_empty(self.description, "description")

        if not self.canonical_id_preserved:
            raise ValueError(
                "canonical_id_preserved must remain true for canonical module graph navigation adapter entries."
            )
        if self.vendor_navigation_id_exposed:
            raise ValueError(
                "vendor_navigation_id_exposed must remain false for canonical module graph navigation adapter entries."
            )
        if not self.navigation_projection_ready:
            raise ValueError(
                "navigation_projection_ready must remain true for canonical module graph navigation adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical module graph navigation adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical module graph navigation adapter entries."
            )


@dataclass(frozen=True, slots=True)
class ModuleGraphNavigationAdapterContract:
    contract_id: str
    total_entries: int
    canonical_id_preserved_entries: int
    navigation_projection_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[ModuleGraphNavigationAdapterEntry, ...]

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
        if self.navigation_projection_ready_entries != sum(
            1 for entry in self.entries if entry.navigation_projection_ready
        ):
            raise ValueError(
                "navigation_projection_ready_entries must match navigation_projection_ready count."
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


def build_module_graph_navigation_adapter_contract() -> ModuleGraphNavigationAdapterContract:
    navigation_contract = build_module_navigation_entry_contract()
    graph_adapter = build_graph_render_adapter_contract()

    entries = tuple(
        ModuleGraphNavigationAdapterEntry(
            adapter_entry_id=f"module_graph_navigation_adapter_{index:03d}",
            module_id=entry.module_id,
            navigation_id=entry.navigation_id,
            navigation_group=entry.navigation_group,
            graph_adapter_contract_id=graph_adapter.contract_id,
            graph_projection_id=f"{entry.module_id}_navigation_graph_projection",
            canonical_id_preserved=True,
            vendor_navigation_id_exposed=False,
            navigation_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical module graph navigation adapter entry for {entry.module_id}.",
        )
        for index, entry in enumerate(navigation_contract.entries, start=1)
    )

    return ModuleGraphNavigationAdapterContract(
        contract_id="module_graph_navigation_adapter_contract_001",
        total_entries=len(entries),
        canonical_id_preserved_entries=sum(
            1 for entry in entries if entry.canonical_id_preserved
        ),
        navigation_projection_ready_entries=sum(
            1 for entry in entries if entry.navigation_projection_ready
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
