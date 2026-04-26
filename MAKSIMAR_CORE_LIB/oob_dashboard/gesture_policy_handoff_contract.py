from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_adapter_contract import (
    build_gesture_adapter_contract,
)


GestureHandoffMode = Literal[
    "gesture_policy_handoff_ready",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GesturePolicyHandoffEntry:
    handoff_entry_id: str
    adapter_entry_id: str
    handoff_mode: GestureHandoffMode
    policy_bound: bool
    direct_execution_allowed: bool
    approval_required: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.handoff_entry_id, "handoff_entry_id")
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.description, "description")

        if not self.policy_bound:
            raise ValueError(
                "policy_bound must remain true for canonical gesture policy handoff entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical gesture policy handoff entries."
            )
        if not self.approval_required:
            raise ValueError(
                "approval_required must remain true for canonical gesture policy handoff entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical gesture policy handoff entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical gesture policy handoff entries."
            )


@dataclass(frozen=True, slots=True)
class GesturePolicyHandoffContract:
    contract_id: str
    total_entries: int
    policy_bound_entries: int
    approval_required_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[GesturePolicyHandoffEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.policy_bound_entries != sum(
            1 for entry in self.entries if entry.policy_bound
        ):
            raise ValueError("policy_bound_entries must match policy_bound count.")
        if self.approval_required_entries != sum(
            1 for entry in self.entries if entry.approval_required
        ):
            raise ValueError(
                "approval_required_entries must match approval_required count."
            )
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded handoff count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_gesture_policy_handoff_contract() -> GesturePolicyHandoffContract:
    adapter_contract = build_gesture_adapter_contract()

    entries = tuple(
        GesturePolicyHandoffEntry(
            handoff_entry_id=f"gesture_policy_handoff_{index:03d}",
            adapter_entry_id=entry.adapter_entry_id,
            handoff_mode="gesture_policy_handoff_ready",
            policy_bound=True,
            direct_execution_allowed=False,
            approval_required=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical gesture policy handoff entry for {entry.adapter_entry_id}.",
        )
        for index, entry in enumerate(adapter_contract.entries, start=1)
    )

    return GesturePolicyHandoffContract(
        contract_id="gesture_policy_handoff_contract_001",
        total_entries=len(entries),
        policy_bound_entries=sum(1 for entry in entries if entry.policy_bound),
        approval_required_entries=sum(1 for entry in entries if entry.approval_required),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
