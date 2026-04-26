from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MonitorMetadataRole = Literal[
    "foundation_primary_metadata",
    "foundation_secondary_metadata",
    "operator_interaction_metadata",
]

MonitorMetadataState = Literal[
    "monitor_metadata_ready",
]

ALL_MONITOR_METADATA_ROLES: tuple[MonitorMetadataRole, ...] = (
    "foundation_primary_metadata",
    "foundation_secondary_metadata",
    "operator_interaction_metadata",
)

ALL_MONITOR_METADATA_STATES: tuple[MonitorMetadataState, ...] = (
    "monitor_metadata_ready",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class MonitorMetadataEntry:
    """Canonical monitor metadata entry."""

    monitor_id: str
    display_target_id: str
    metadata_role: MonitorMetadataRole
    metadata_state: MonitorMetadataState
    display_role: str
    display_zone: str
    fallback_display_target_id: str
    occupancy_class: str
    assignment_count: int
    supports_foundation_panels: bool
    supports_operator_surfaces: bool
    multi_monitor_capable: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.monitor_id, "monitor_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.display_role, "display_role")
        _require_non_empty(self.display_zone, "display_zone")
        _require_non_empty(
            self.fallback_display_target_id, "fallback_display_target_id"
        )
        _require_non_empty(self.occupancy_class, "occupancy_class")
        _require_non_empty(self.description, "description")

        if self.metadata_role not in ALL_MONITOR_METADATA_ROLES:
            raise ValueError(
                "metadata_role must be one of "
                f"{ALL_MONITOR_METADATA_ROLES}, got {self.metadata_role!r}."
            )

        if self.metadata_state not in ALL_MONITOR_METADATA_STATES:
            raise ValueError(
                "metadata_state must be one of "
                f"{ALL_MONITOR_METADATA_STATES}, got {self.metadata_state!r}."
            )

        if self.assignment_count < 1:
            raise ValueError("assignment_count must be >= 1.")

        if not self.multi_monitor_capable:
            raise ValueError(
                "multi_monitor_capable must remain true for canonical monitor metadata."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical monitor metadata."
            )

        if (
            self.metadata_role == "operator_interaction_metadata"
            and not self.supports_operator_surfaces
        ):
            raise ValueError(
                "operator_interaction_metadata must support operator surfaces."
            )

        if (
            self.metadata_role != "operator_interaction_metadata"
            and not self.supports_foundation_panels
        ):
            raise ValueError(
                "foundation metadata roles must support foundation panels."
            )


@dataclass(frozen=True, slots=True)
class MonitorMetadataContract:
    """Canonical monitor metadata contract."""

    contract_id: str
    total_entries: int
    foundation_metadata_entries: int
    operator_metadata_entries: int
    operator_visible_entries: int
    entries: tuple[MonitorMetadataEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.foundation_metadata_entries != sum(
            1
            for entry in self.entries
            if entry.metadata_role in {
                "foundation_primary_metadata",
                "foundation_secondary_metadata",
            }
        ):
            raise ValueError(
                "foundation_metadata_entries must match foundation metadata count."
            )

        if self.operator_metadata_entries != sum(
            1
            for entry in self.entries
            if entry.metadata_role == "operator_interaction_metadata"
        ):
            raise ValueError(
                "operator_metadata_entries must match operator metadata count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )
