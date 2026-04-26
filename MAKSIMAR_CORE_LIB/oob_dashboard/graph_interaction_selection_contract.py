from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_interaction_policy_contract import (
    build_graph_interaction_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_non_execution_guard_contract import (
    build_graph_non_execution_guard_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GraphInteractionSelectionEntry:
    selection_entry_id: str
    interaction_kind: str
    selection_scope: str
    inspect_surface_id: str
    selection_ready: bool
    inspect_only: bool
    execution_path_open: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.selection_entry_id, "selection_entry_id")
        _require_non_empty(self.interaction_kind, "interaction_kind")
        _require_non_empty(self.selection_scope, "selection_scope")
        _require_non_empty(self.inspect_surface_id, "inspect_surface_id")
        _require_non_empty(self.description, "description")

        if not self.selection_ready:
            raise ValueError(
                "selection_ready must remain true for canonical graph interaction selection entries."
            )
        if not self.inspect_only:
            raise ValueError(
                "inspect_only must remain true for canonical graph interaction selection entries."
            )
        if self.execution_path_open:
            raise ValueError(
                "execution_path_open must remain false for canonical graph interaction selection entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical graph interaction selection entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical graph interaction selection entries."
            )


@dataclass(frozen=True, slots=True)
class GraphInteractionSelectionContract:
    contract_id: str
    total_entries: int
    selection_ready_entries: int
    inspect_only_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[GraphInteractionSelectionEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.selection_ready_entries != sum(
            1 for entry in self.entries if entry.selection_ready
        ):
            raise ValueError(
                "selection_ready_entries must match selection_ready count."
            )
        if self.inspect_only_entries != sum(
            1 for entry in self.entries if entry.inspect_only
        ):
            raise ValueError("inspect_only_entries must match inspect_only count.")
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


def build_graph_interaction_selection_contract() -> GraphInteractionSelectionContract:
    policy_contract = build_graph_interaction_policy_contract()
    guard_contract = build_graph_non_execution_guard_contract()

    if guard_contract.execution_forbidden_entries != policy_contract.total_entries:
        raise ValueError(
            "guard contract must fully cover all graph interaction policy entries."
        )

    inspect_surface_map = {
        "graph_select": "graph_inspect_primary_surface",
        "graph_zoom": "graph_zoom_inspect_surface",
        "graph_pan": "graph_pan_inspect_surface",
    }

    entries = tuple(
        GraphInteractionSelectionEntry(
            selection_entry_id=f"graph_interaction_selection_{index:03d}",
            interaction_kind=entry.interaction_kind,
            selection_scope=entry.selection_scope,
            inspect_surface_id=inspect_surface_map[entry.interaction_kind],
            selection_ready=True,
            inspect_only=True,
            execution_path_open=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical graph interaction selection entry for {entry.interaction_kind}.",
        )
        for index, entry in enumerate(policy_contract.entries, start=1)
    )

    return GraphInteractionSelectionContract(
        contract_id="graph_interaction_selection_contract_001",
        total_entries=len(entries),
        selection_ready_entries=sum(1 for entry in entries if entry.selection_ready),
        inspect_only_entries=sum(1 for entry in entries if entry.inspect_only),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
