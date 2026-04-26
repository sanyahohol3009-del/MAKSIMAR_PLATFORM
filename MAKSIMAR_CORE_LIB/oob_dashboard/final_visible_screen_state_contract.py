from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_contract import (
    build_presentation_bundle_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.rollback_readiness_contract import (
    build_rollback_readiness_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class FinalVisibleScreenStateEntry:
    """Canonical final visible screen state entry."""

    final_visible_screen_state_id: str
    display_target_id: str
    workspace_id: str
    final_visible_screen_state: str
    final_visible_screen_state_class: str
    presentation_bundle_ready: bool
    rollback_readiness_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(
            self.final_visible_screen_state_id,
            "final_visible_screen_state_id",
        )
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(
            self.final_visible_screen_state,
            "final_visible_screen_state",
        )
        _require_non_empty(
            self.final_visible_screen_state_class,
            "final_visible_screen_state_class",
        )
        _require_non_empty(self.description, "description")

        if self.final_visible_screen_state != "final_visible_screen_state_ready":
            raise ValueError(
                "final_visible_screen_state must remain final_visible_screen_state_ready."
            )

        if self.final_visible_screen_state_class not in {
            "foundation_primary_final_screen_state",
            "foundation_secondary_final_screen_state",
            "interaction_final_screen_state",
        }:
            raise ValueError(
                "final_visible_screen_state_class must be one of "
                "{foundation_primary_final_screen_state, "
                "foundation_secondary_final_screen_state, "
                "interaction_final_screen_state}."
            )

        if not self.presentation_bundle_ready:
            raise ValueError(
                "presentation_bundle_ready must remain true for canonical final visible screen state."
            )

        if not self.rollback_readiness_ready:
            raise ValueError(
                "rollback_readiness_ready must remain true for canonical final visible screen state."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical final visible screen state."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical final visible screen state."
            )


@dataclass(frozen=True, slots=True)
class FinalVisibleScreenStateContract:
    """Canonical final visible screen state contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[FinalVisibleScreenStateEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.final_visible_screen_state == "final_visible_screen_state_ready"
        ):
            raise ValueError(
                "ready_entries must match final_visible_screen_state_ready count."
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
            raise ValueError(
                "truth_bound_entries must match truth_bound count."
            )


def build_final_visible_screen_state_contract() -> FinalVisibleScreenStateContract:
    """Build canonical final visible screen state contract."""
    presentation_bundle_contract = build_presentation_bundle_contract()
    rollback_readiness_contract = build_rollback_readiness_contract()

    presentation_bundle_ready = bool(presentation_bundle_contract.entries)
    rollback_readiness_ready = bool(rollback_readiness_contract.entries)

    class_map = {
        "display_foundation_primary": "foundation_primary_final_screen_state",
        "display_foundation_secondary": "foundation_secondary_final_screen_state",
        "display_operator_interaction": "interaction_final_screen_state",
    }

    entries = tuple(
        FinalVisibleScreenStateEntry(
            final_visible_screen_state_id=f"final_visible_screen_state_{index:03d}",
            display_target_id=entry.display_target_id,
            workspace_id=entry.workspace_id,
            final_visible_screen_state="final_visible_screen_state_ready",
            final_visible_screen_state_class=class_map[entry.display_target_id],
            presentation_bundle_ready=presentation_bundle_ready,
            rollback_readiness_ready=rollback_readiness_ready,
            operator_visible=entry.operator_visible,
            truth_bound=entry.truth_bound,
            description=(
                "Canonical final visible screen state entry for "
                f"{entry.display_target_id}."
            ),
        )
        for index, entry in enumerate(
            presentation_bundle_contract.entries,
            start=1,
        )
    )

    return FinalVisibleScreenStateContract(
        contract_id="final_visible_screen_state_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.final_visible_screen_state == "final_visible_screen_state_ready"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
