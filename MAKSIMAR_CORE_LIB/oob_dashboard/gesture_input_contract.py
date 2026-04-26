from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


GestureInputKind = Literal[
    "gesture_pointer_input",
    "gesture_confirm_input",
    "gesture_navigation_input",
]

GestureInputState = Literal[
    "gesture_input_ready",
]


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class GestureInputEntry:
    gesture_input_id: str
    gesture_kind: GestureInputKind
    source_device_id: str
    normalized_input_ready: bool
    direct_action_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.gesture_input_id, "gesture_input_id")
        _require_non_empty(self.source_device_id, "source_device_id")
        _require_non_empty(self.description, "description")

        if not self.normalized_input_ready:
            raise ValueError(
                "normalized_input_ready must remain true for canonical gesture input entries."
            )
        if self.direct_action_allowed:
            raise ValueError(
                "direct_action_allowed must remain false for canonical gesture input entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical gesture input entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical gesture input entries."
            )


@dataclass(frozen=True, slots=True)
class GestureInputContract:
    contract_id: str
    state: GestureInputState
    total_entries: int
    normalized_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[GestureInputEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.normalized_entries != sum(
            1 for entry in self.entries if entry.normalized_input_ready
        ):
            raise ValueError("normalized_entries must match normalized_input_ready count.")
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_action_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded gesture count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_gesture_input_contract() -> GestureInputContract:
    entries = (
        GestureInputEntry(
            gesture_input_id="gesture_input_001",
            gesture_kind="gesture_pointer_input",
            source_device_id="gesture_sensor_primary",
            normalized_input_ready=True,
            direct_action_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical pointer-style gesture input entry.",
        ),
        GestureInputEntry(
            gesture_input_id="gesture_input_002",
            gesture_kind="gesture_confirm_input",
            source_device_id="gesture_sensor_primary",
            normalized_input_ready=True,
            direct_action_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical confirm-style gesture input entry.",
        ),
        GestureInputEntry(
            gesture_input_id="gesture_input_003",
            gesture_kind="gesture_navigation_input",
            source_device_id="gesture_sensor_primary",
            normalized_input_ready=True,
            direct_action_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical navigation-style gesture input entry.",
        ),
    )

    return GestureInputContract(
        contract_id="gesture_input_contract_001",
        state="gesture_input_ready",
        total_entries=len(entries),
        normalized_entries=sum(1 for entry in entries if entry.normalized_input_ready),
        guarded_entries=sum(1 for entry in entries if entry.direct_action_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
