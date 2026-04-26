from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_visible_state_contract import (
    build_dashboard_visible_state_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_restore_contract import (
    build_display_assignment_restore_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_placement_restore_contract import (
    build_panel_placement_restore_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PresentationBundleEntry:
    """Canonical presentation bundle entry."""

    presentation_bundle_id: str
    workspace_id: str
    display_target_id: str
    panel_or_surface_id: str
    presentation_bundle_state: str
    presentation_bundle_class: str
    dashboard_visible_state_ready: bool
    display_mapping_consistent: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.presentation_bundle_id, "presentation_bundle_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.panel_or_surface_id, "panel_or_surface_id")
        _require_non_empty(
            self.presentation_bundle_state,
            "presentation_bundle_state",
        )
        _require_non_empty(
            self.presentation_bundle_class,
            "presentation_bundle_class",
        )
        _require_non_empty(self.description, "description")

        if self.presentation_bundle_state != "presentation_bundle_ready":
            raise ValueError(
                "presentation_bundle_state must remain presentation_bundle_ready."
            )

        if self.presentation_bundle_class not in {
            "primary_presentation_bundle",
            "secondary_presentation_bundle",
            "interaction_presentation_bundle",
        }:
            raise ValueError(
                "presentation_bundle_class must be one of "
                "{primary_presentation_bundle, secondary_presentation_bundle, "
                "interaction_presentation_bundle}."
            )

        if not self.dashboard_visible_state_ready:
            raise ValueError(
                "dashboard_visible_state_ready must remain true for canonical presentation bundles."
            )

        if not self.display_mapping_consistent:
            raise ValueError(
                "display_mapping_consistent must remain true for canonical presentation bundles."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical presentation bundles."
            )

        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical presentation bundles."
            )


@dataclass(frozen=True, slots=True)
class PresentationBundleContract:
    """Canonical presentation bundle contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[PresentationBundleEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.ready_entries != sum(
            1
            for entry in self.entries
            if entry.presentation_bundle_state == "presentation_bundle_ready"
        ):
            raise ValueError(
                "ready_entries must match presentation_bundle_ready count."
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


def build_presentation_bundle_contract() -> PresentationBundleContract:
    """Build canonical presentation bundle contract."""
    dashboard_visible_state_contract = build_dashboard_visible_state_contract()
    display_assignment_restore_contract = build_display_assignment_restore_contract()
    panel_placement_restore_contract = build_panel_placement_restore_contract()

    dashboard_visible_state_ready = bool(dashboard_visible_state_contract.entries)
    panel_restore_workspace_id = panel_placement_restore_contract.entries[0].workspace_id

    class_map = {
        "display_foundation_primary": "primary_presentation_bundle",
        "display_foundation_secondary": "secondary_presentation_bundle",
        "display_operator_interaction": "interaction_presentation_bundle",
    }

    entries = tuple(
        PresentationBundleEntry(
            presentation_bundle_id=f"presentation_bundle_{index:03d}",
            workspace_id=entry.workspace_id,
            display_target_id=entry.display_target_id,
            panel_or_surface_id=entry.panel_or_surface_id,
            presentation_bundle_state="presentation_bundle_ready",
            presentation_bundle_class=class_map[entry.display_target_id],
            dashboard_visible_state_ready=dashboard_visible_state_ready,
            display_mapping_consistent=(
                entry.workspace_id == panel_restore_workspace_id
                or entry.display_target_id == "display_operator_interaction"
            ),
            operator_visible=entry.operator_visible,
            truth_bound=True,
            description=(
                "Canonical presentation bundle entry for "
                f"{entry.display_target_id}."
            ),
        )
        for index, entry in enumerate(
            display_assignment_restore_contract.entries,
            start=1,
        )
    )

    return PresentationBundleContract(
        contract_id="presentation_bundle_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.presentation_bundle_state == "presentation_bundle_ready"
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        truth_bound_entries=sum(
            1 for entry in entries if entry.truth_bound
        ),
        entries=entries,
    )
