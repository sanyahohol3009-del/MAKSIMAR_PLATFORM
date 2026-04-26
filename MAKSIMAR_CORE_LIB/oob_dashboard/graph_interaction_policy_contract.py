from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_selection_mapping_contract import (
    build_graph_selection_mapping_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GraphInteractionPolicyEntry:
    policy_entry_id: str
    interaction_kind: str
    selection_scope: str
    allowed: bool
    inspect_only: bool
    mutates_runtime: bool
    bypasses_control_plane: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.policy_entry_id, "policy_entry_id")
        _require_non_empty(self.interaction_kind, "interaction_kind")
        _require_non_empty(self.selection_scope, "selection_scope")
        _require_non_empty(self.description, "description")

        if not self.allowed:
            raise ValueError(
                "allowed must remain true for canonical graph interaction policy entries."
            )
        if not self.inspect_only:
            raise ValueError(
                "inspect_only must remain true for canonical graph interaction policy entries."
            )
        if self.mutates_runtime:
            raise ValueError(
                "mutates_runtime must remain false for canonical graph interaction policy entries."
            )
        if self.bypasses_control_plane:
            raise ValueError(
                "bypasses_control_plane must remain false for canonical graph interaction policy entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical graph interaction policy entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical graph interaction policy entries."
            )


@dataclass(frozen=True, slots=True)
class GraphInteractionPolicyContract:
    contract_id: str
    total_entries: int
    allowed_entries: int
    inspect_only_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[GraphInteractionPolicyEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.allowed_entries != sum(1 for entry in self.entries if entry.allowed):
            raise ValueError("allowed_entries must match allowed count.")
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


def build_graph_interaction_policy_contract() -> GraphInteractionPolicyContract:
    selection_contract = build_graph_selection_mapping_contract()

    interaction_kinds = (
        "graph_select",
        "graph_zoom",
        "graph_pan",
    )

    entries = tuple(
        GraphInteractionPolicyEntry(
            policy_entry_id=f"graph_interaction_policy_{index:03d}",
            interaction_kind=interaction_kind,
            selection_scope=selection_contract.entries[index - 1].selection_scope,
            allowed=True,
            inspect_only=True,
            mutates_runtime=False,
            bypasses_control_plane=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical graph interaction policy entry for {interaction_kind}.",
        )
        for index, interaction_kind in enumerate(interaction_kinds, start=1)
    )

    return GraphInteractionPolicyContract(
        contract_id="graph_interaction_policy_contract_001",
        total_entries=len(entries),
        allowed_entries=sum(1 for entry in entries if entry.allowed),
        inspect_only_entries=sum(1 for entry in entries if entry.inspect_only),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
