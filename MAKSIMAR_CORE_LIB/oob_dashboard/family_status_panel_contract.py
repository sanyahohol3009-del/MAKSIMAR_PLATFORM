from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class FamilyStatusPanelEntry:
    family_member_id: str
    family_role: str
    family_state: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.family_member_id, "family_member_id")
        _require_non_empty(self.family_role, "family_role")
        _require_non_empty(self.family_state, "family_state")
        _require_non_empty(self.description, "description")

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical family-status panel entries."
            )


@dataclass(frozen=True, slots=True)
class FamilyStatusPanelContract:
    panel_id: str
    total_entries: int
    operator_visible_entries: int
    entries: Tuple[FamilyStatusPanelEntry, ...]
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical family-status panel contract."
            )


def build_family_status_panel_contract() -> FamilyStatusPanelContract:
    entries = (
        FamilyStatusPanelEntry(
            family_member_id="family_guardian_primary",
            family_role="guardian",
            family_state="active_guardian_context",
            operator_visible=True,
            description="Canonical primary guardian family status.",
        ),
        FamilyStatusPanelEntry(
            family_member_id="family_child_monitoring",
            family_role="child_monitoring",
            family_state="protected_monitoring_context",
            operator_visible=True,
            description="Canonical child-monitoring family status.",
        ),
        FamilyStatusPanelEntry(
            family_member_id="family_assistant_core",
            family_role="assistant",
            family_state="family_safe_mode",
            operator_visible=True,
            description="Canonical family assistant safety status.",
        ),
    )

    return FamilyStatusPanelContract(
        panel_id="panel_family_status",
        total_entries=len(entries),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
        operator_visible=True,
        description="Canonical family-status panel contract.",
    )
