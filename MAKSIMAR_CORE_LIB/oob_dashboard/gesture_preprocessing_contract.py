from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.gesture_input_contract import (
    build_gesture_input_contract,
)


GesturePreprocessingMode = Literal[
    "gesture_preprocessing_ready",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GesturePreprocessingEntry:
    preprocessing_id: str
    gesture_input_id: str
    noise_filtered: bool
    structurally_valid: bool
    direct_execution_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.preprocessing_id, "preprocessing_id")
        _require_non_empty(self.gesture_input_id, "gesture_input_id")
        _require_non_empty(self.description, "description")

        if not self.noise_filtered:
            raise ValueError(
                "noise_filtered must remain true for canonical gesture preprocessing entries."
            )
        if not self.structurally_valid:
            raise ValueError(
                "structurally_valid must remain true for canonical gesture preprocessing entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical gesture preprocessing entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical gesture preprocessing entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical gesture preprocessing entries."
            )


@dataclass(frozen=True, slots=True)
class GesturePreprocessingContract:
    contract_id: str
    mode: GesturePreprocessingMode
    total_entries: int
    valid_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[GesturePreprocessingEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.valid_entries != sum(
            1 for entry in self.entries if entry.noise_filtered and entry.structurally_valid
        ):
            raise ValueError("valid_entries must match preprocessing validity count.")
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded preprocessing count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_gesture_preprocessing_contract() -> GesturePreprocessingContract:
    input_contract = build_gesture_input_contract()

    entries = tuple(
        GesturePreprocessingEntry(
            preprocessing_id=f"gesture_preprocessing_{index:03d}",
            gesture_input_id=entry.gesture_input_id,
            noise_filtered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical gesture preprocessing entry for {entry.gesture_input_id}.",
        )
        for index, entry in enumerate(input_contract.entries, start=1)
    )

    return GesturePreprocessingContract(
        contract_id="gesture_preprocessing_contract_001",
        mode="gesture_preprocessing_ready",
        total_entries=len(entries),
        valid_entries=sum(
            1 for entry in entries if entry.noise_filtered and entry.structurally_valid
        ),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
