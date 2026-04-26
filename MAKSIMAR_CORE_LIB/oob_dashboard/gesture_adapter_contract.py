from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_preprocessing_contract import (
    build_gesture_preprocessing_contract,
)


GestureAdapterTarget = Literal[
    "panel_gesture_control",
    "panel_operator_main",
    "panel_command_strip",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GestureAdapterEntry:
    adapter_entry_id: str
    preprocessing_id: str
    target_panel_id: GestureAdapterTarget
    adapted_to_operator_intent: bool
    direct_action_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.adapter_entry_id, "adapter_entry_id")
        _require_non_empty(self.preprocessing_id, "preprocessing_id")
        _require_non_empty(self.description, "description")

        if not self.adapted_to_operator_intent:
            raise ValueError(
                "adapted_to_operator_intent must remain true for canonical gesture adapter entries."
            )
        if self.direct_action_allowed:
            raise ValueError(
                "direct_action_allowed must remain false for canonical gesture adapter entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical gesture adapter entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical gesture adapter entries."
            )


@dataclass(frozen=True, slots=True)
class GestureAdapterContract:
    contract_id: str
    total_entries: int
    adapted_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[GestureAdapterEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.adapted_entries != sum(
            1 for entry in self.entries if entry.adapted_to_operator_intent
        ):
            raise ValueError("adapted_entries must match adapted_to_operator_intent count.")
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_action_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded gesture adapter count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_gesture_adapter_contract() -> GestureAdapterContract:
    preprocessing_contract = build_gesture_preprocessing_contract()
    target_order: tuple[GestureAdapterTarget, ...] = (
        "panel_gesture_control",
        "panel_operator_main",
        "panel_command_strip",
    )

    entries = tuple(
        GestureAdapterEntry(
            adapter_entry_id=f"gesture_adapter_{index:03d}",
            preprocessing_id=entry.preprocessing_id,
            target_panel_id=target_order[index - 1],
            adapted_to_operator_intent=True,
            direct_action_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical gesture adapter entry for {entry.preprocessing_id}.",
        )
        for index, entry in enumerate(preprocessing_contract.entries, start=1)
    )

    return GestureAdapterContract(
        contract_id="gesture_adapter_contract_001",
        total_entries=len(entries),
        adapted_entries=sum(1 for entry in entries if entry.adapted_to_operator_intent),
        guarded_entries=sum(1 for entry in entries if entry.direct_action_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
