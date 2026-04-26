from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_conflict_resolution_contract import (
    build_display_conflict_resolution_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.logical_display_target_contract import (
    build_logical_display_target_contract,
)


OperatorCloseOrReplaceDecisionState = Literal[
    "operator_decision_ready",
]

OperatorCloseOrReplaceDecisionClass = Literal[
    "retain_primary_surface_decision",
    "replace_secondary_surface_decision",
]

OperatorCloseOrReplaceAction = Literal[
    "retain_current_surface",
    "replace_with_candidate_surface",
]

ALL_OPERATOR_CLOSE_OR_REPLACE_DECISION_STATES: tuple[
    OperatorCloseOrReplaceDecisionState, ...
] = ("operator_decision_ready",)

ALL_OPERATOR_CLOSE_OR_REPLACE_DECISION_CLASSES: tuple[
    OperatorCloseOrReplaceDecisionClass, ...
] = (
    "retain_primary_surface_decision",
    "replace_secondary_surface_decision",
)

ALL_OPERATOR_CLOSE_OR_REPLACE_ACTIONS: tuple[
    OperatorCloseOrReplaceAction, ...
] = (
    "retain_current_surface",
    "replace_with_candidate_surface",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class OperatorCloseOrReplaceDecisionEntry:
    """Canonical operator close-or-replace decision entry."""

    decision_id: str
    display_target_id: str
    logical_target_id: str
    decision_state: OperatorCloseOrReplaceDecisionState
    decision_class: OperatorCloseOrReplaceDecisionClass
    decision_action: OperatorCloseOrReplaceAction
    candidate_display_target_id: str | None
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.decision_id, "decision_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.logical_target_id, "logical_target_id")
        _require_non_empty(self.description, "description")

        if self.decision_state not in ALL_OPERATOR_CLOSE_OR_REPLACE_DECISION_STATES:
            raise ValueError(
                "decision_state must be one of "
                f"{ALL_OPERATOR_CLOSE_OR_REPLACE_DECISION_STATES}, got {self.decision_state!r}."
            )

        if self.decision_class not in ALL_OPERATOR_CLOSE_OR_REPLACE_DECISION_CLASSES:
            raise ValueError(
                "decision_class must be one of "
                f"{ALL_OPERATOR_CLOSE_OR_REPLACE_DECISION_CLASSES}, got {self.decision_class!r}."
            )

        if self.decision_action not in ALL_OPERATOR_CLOSE_OR_REPLACE_ACTIONS:
            raise ValueError(
                "decision_action must be one of "
                f"{ALL_OPERATOR_CLOSE_OR_REPLACE_ACTIONS}, got {self.decision_action!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical operator close-or-replace decisions."
            )

        if (
            self.decision_action == "retain_current_surface"
            and self.candidate_display_target_id is not None
        ):
            raise ValueError(
                "retain_current_surface entries must not expose candidate_display_target_id."
            )

        if (
            self.decision_action == "replace_with_candidate_surface"
            and (
                self.candidate_display_target_id is None
                or not self.candidate_display_target_id.strip()
            )
        ):
            raise ValueError(
                "replace_with_candidate_surface entries must expose candidate_display_target_id."
            )


@dataclass(frozen=True, slots=True)
class OperatorCloseOrReplaceDecisionContract:
    """Canonical operator close-or-replace decision contract."""

    contract_id: str
    total_entries: int
    retain_entries: int
    replace_entries: int
    operator_visible_entries: int
    entries: tuple[OperatorCloseOrReplaceDecisionEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.retain_entries != sum(
            1
            for entry in self.entries
            if entry.decision_action == "retain_current_surface"
        ):
            raise ValueError("retain_entries must match retain_current_surface count.")

        if self.replace_entries != sum(
            1
            for entry in self.entries
            if entry.decision_action == "replace_with_candidate_surface"
        ):
            raise ValueError(
                "replace_entries must match replace_with_candidate_surface count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_operator_close_or_replace_decision_contract() -> (
    OperatorCloseOrReplaceDecisionContract
):
    """Build canonical operator close-or-replace decision contract."""
    conflict_contract = build_display_conflict_resolution_contract()
    logical_target_contract = build_logical_display_target_contract()

    logical_target_by_display = {
        entry.display_target_id: entry for entry in logical_target_contract.entries
    }

    class_map: dict[str, OperatorCloseOrReplaceDecisionClass] = {
        "display_foundation_primary": "retain_primary_surface_decision",
        "display_foundation_secondary": "replace_secondary_surface_decision",
    }

    action_map: dict[str, OperatorCloseOrReplaceAction] = {
        "retain_pinned_surface": "retain_current_surface",
        "replace_replaceable_surface": "replace_with_candidate_surface",
    }

    ordered_display_targets = (
        "display_foundation_primary",
        "display_foundation_secondary",
    )

    conflict_by_display = {
        entry.display_target_id: entry for entry in conflict_contract.entries
    }

    entries = tuple(
        OperatorCloseOrReplaceDecisionEntry(
            decision_id=f"operator_close_or_replace_decision_{index:03d}",
            display_target_id=display_target_id,
            logical_target_id=logical_target_by_display[
                display_target_id
            ].logical_target_id,
            decision_state="operator_decision_ready",
            decision_class=class_map[display_target_id],
            decision_action=action_map[
                conflict_by_display[display_target_id].conflict_decision
            ],
            candidate_display_target_id=conflict_by_display[
                display_target_id
            ].candidate_display_target_id,
            operator_visible=True,
            description=(
                f"Canonical operator close-or-replace decision entry for {display_target_id}."
            ),
        )
        for index, display_target_id in enumerate(ordered_display_targets, start=1)
    )

    return OperatorCloseOrReplaceDecisionContract(
        contract_id="operator_close_or_replace_decision_contract_001",
        total_entries=len(entries),
        retain_entries=sum(
            1
            for entry in entries
            if entry.decision_action == "retain_current_surface"
        ),
        replace_entries=sum(
            1
            for entry in entries
            if entry.decision_action == "replace_with_candidate_surface"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
