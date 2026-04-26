from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_interaction_policy_contract import (
    build_graph_interaction_policy_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GraphNonExecutionGuardEntry:
    guard_entry_id: str
    interaction_kind: str
    execution_forbidden: bool
    runtime_write_forbidden: bool
    control_plane_bypass_forbidden: bool
    safe_preview_only: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.guard_entry_id, "guard_entry_id")
        _require_non_empty(self.interaction_kind, "interaction_kind")
        _require_non_empty(self.description, "description")

        if not self.execution_forbidden:
            raise ValueError(
                "execution_forbidden must remain true for canonical graph non-execution guard entries."
            )
        if not self.runtime_write_forbidden:
            raise ValueError(
                "runtime_write_forbidden must remain true for canonical graph non-execution guard entries."
            )
        if not self.control_plane_bypass_forbidden:
            raise ValueError(
                "control_plane_bypass_forbidden must remain true for canonical graph non-execution guard entries."
            )
        if not self.safe_preview_only:
            raise ValueError(
                "safe_preview_only must remain true for canonical graph non-execution guard entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical graph non-execution guard entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical graph non-execution guard entries."
            )


@dataclass(frozen=True, slots=True)
class GraphNonExecutionGuardContract:
    contract_id: str
    total_entries: int
    execution_forbidden_entries: int
    safe_preview_only_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: Tuple[GraphNonExecutionGuardEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.execution_forbidden_entries != sum(
            1 for entry in self.entries if entry.execution_forbidden
        ):
            raise ValueError(
                "execution_forbidden_entries must match execution_forbidden count."
            )
        if self.safe_preview_only_entries != sum(
            1 for entry in self.entries if entry.safe_preview_only
        ):
            raise ValueError(
                "safe_preview_only_entries must match safe_preview_only count."
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


def build_graph_non_execution_guard_contract() -> GraphNonExecutionGuardContract:
    policy_contract = build_graph_interaction_policy_contract()

    entries = tuple(
        GraphNonExecutionGuardEntry(
            guard_entry_id=f"graph_non_execution_guard_{index:03d}",
            interaction_kind=entry.interaction_kind,
            execution_forbidden=True,
            runtime_write_forbidden=True,
            control_plane_bypass_forbidden=True,
            safe_preview_only=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical graph non-execution guard entry for {entry.interaction_kind}.",
        )
        for index, entry in enumerate(policy_contract.entries, start=1)
    )

    return GraphNonExecutionGuardContract(
        contract_id="graph_non_execution_guard_contract_001",
        total_entries=len(entries),
        execution_forbidden_entries=sum(
            1 for entry in entries if entry.execution_forbidden
        ),
        safe_preview_only_entries=sum(
            1 for entry in entries if entry.safe_preview_only
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
