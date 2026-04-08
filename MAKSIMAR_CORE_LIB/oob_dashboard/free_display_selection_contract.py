from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_occupancy_contract import (
    build_display_occupancy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_replacement_policy_contract import (
    build_display_replacement_policy_contract,
)


SelectionDecision = Literal[
    "replaceable_display_candidate_available",
    "no_free_display_available",
]

SelectionReason = Literal[
    "replaceable_secondary_or_tertiary_available",
    "no_replaceable_display_available",
]

RequestedRoleHint = Literal[
    "operator_auxiliary_surface",
]

ALL_SELECTION_DECISIONS: tuple[SelectionDecision, ...] = (
    "replaceable_display_candidate_available",
    "no_free_display_available",
)

ALL_SELECTION_REASONS: tuple[SelectionReason, ...] = (
    "replaceable_secondary_or_tertiary_available",
    "no_replaceable_display_available",
)

ALL_REQUESTED_ROLE_HINTS: tuple[RequestedRoleHint, ...] = (
    "operator_auxiliary_surface",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class FreeDisplaySelectionEntry:
    """Canonical free display selection entry."""

    selection_id: str
    requested_role_hint: RequestedRoleHint
    selection_decision: SelectionDecision
    selection_reason: SelectionReason
    candidate_display_target_id: str | None
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical free display selection entry."""
        _require_non_empty(self.selection_id, "selection_id")
        _require_non_empty(self.description, "description")

        if self.requested_role_hint not in ALL_REQUESTED_ROLE_HINTS:
            raise ValueError(
                "requested_role_hint must be one of "
                f"{ALL_REQUESTED_ROLE_HINTS}, got {self.requested_role_hint!r}."
            )

        if self.selection_decision not in ALL_SELECTION_DECISIONS:
            raise ValueError(
                "selection_decision must be one of "
                f"{ALL_SELECTION_DECISIONS}, got {self.selection_decision!r}."
            )

        if self.selection_reason not in ALL_SELECTION_REASONS:
            raise ValueError(
                "selection_reason must be one of "
                f"{ALL_SELECTION_REASONS}, got {self.selection_reason!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical free display selection entries."
            )

        if (
            self.selection_decision == "no_free_display_available"
            and self.candidate_display_target_id is not None
        ):
            raise ValueError(
                "no_free_display_available entries must not expose candidate_display_target_id."
            )

        if (
            self.selection_decision == "replaceable_display_candidate_available"
            and (self.candidate_display_target_id is None or not self.candidate_display_target_id.strip())
        ):
            raise ValueError(
                "replaceable_display_candidate_available entries must include candidate_display_target_id."
            )

        if (
            self.selection_decision == "replaceable_display_candidate_available"
            and self.selection_reason != "replaceable_secondary_or_tertiary_available"
        ):
            raise ValueError(
                "replaceable_display_candidate_available entries must use selection_reason='replaceable_secondary_or_tertiary_available'."
            )

        if (
            self.selection_decision == "no_free_display_available"
            and self.selection_reason != "no_replaceable_display_available"
        ):
            raise ValueError(
                "no_free_display_available entries must use selection_reason='no_replaceable_display_available'."
            )


@dataclass(frozen=True, slots=True)
class FreeDisplaySelectionContract:
    """Canonical free display selection contract."""

    contract_id: str
    total_entries: int
    no_free_display_entries: int
    replaceable_candidate_entries: int
    operator_visible_entries: int
    entries: tuple[FreeDisplaySelectionEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical free display selection contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match number of entries.")

        if self.no_free_display_entries != sum(
            1
            for entry in self.entries
            if entry.selection_decision == "no_free_display_available"
        ):
            raise ValueError("no_free_display_entries mismatch.")

        if self.replaceable_candidate_entries != sum(
            1
            for entry in self.entries
            if entry.selection_decision == "replaceable_display_candidate_available"
        ):
            raise ValueError("replaceable_candidate_entries mismatch.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries mismatch.")


def _resolve_candidate_display_target_id() -> str | None:
    """Resolve a replaceable candidate display target from canonical display contracts."""
    occupancy_contract = build_display_occupancy_contract()
    replacement_policy_contract = build_display_replacement_policy_contract()

    replaceable_by_display = {
        entry.display_target_id
        for entry in replacement_policy_contract.entries
        if entry.replacement_decision == "replaceable_without_disruption"
    }

    occupancy_priority = {
        "display_secondary_diagnostics": 1,
        "display_tertiary_expansion": 2,
    }

    eligible_displays = [
        entry.display_target_id
        for entry in occupancy_contract.entries
        if entry.display_target_id in replaceable_by_display
        and entry.occupancy_state == "occupied_replaceable"
    ]

    eligible_displays.sort(
        key=lambda display_id: occupancy_priority.get(display_id, 99)
    )

    return eligible_displays[0] if eligible_displays else None


def build_free_display_selection_contract() -> FreeDisplaySelectionContract:
    """Build canonical free display selection contract."""
    candidate_display_target_id = _resolve_candidate_display_target_id()

    if candidate_display_target_id is None:
        entry = FreeDisplaySelectionEntry(
            selection_id="free_display_selection_001",
            requested_role_hint="operator_auxiliary_surface",
            selection_decision="no_free_display_available",
            selection_reason="no_replaceable_display_available",
            candidate_display_target_id=None,
            operator_visible=True,
            description=(
                "Canonical free display selection entry with no replaceable display candidate available."
            ),
        )
    else:
        entry = FreeDisplaySelectionEntry(
            selection_id="free_display_selection_001",
            requested_role_hint="operator_auxiliary_surface",
            selection_decision="replaceable_display_candidate_available",
            selection_reason="replaceable_secondary_or_tertiary_available",
            candidate_display_target_id=candidate_display_target_id,
            operator_visible=True,
            description=(
                "Canonical free display selection entry resolved from replaceable display occupancy and replacement policy."
            ),
        )

    entries = (entry,)

    return FreeDisplaySelectionContract(
        contract_id="free_display_selection_contract_001",
        total_entries=1,
        no_free_display_entries=sum(
            1
            for entry in entries
            if entry.selection_decision == "no_free_display_available"
        ),
        replaceable_candidate_entries=sum(
            1
            for entry in entries
            if entry.selection_decision == "replaceable_display_candidate_available"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
