from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_metadata_models import (
    MonitorMetadataEntry,
)


def test_monitor_metadata_entry_accepts_foundation_metadata() -> None:
    """Foundation monitor metadata entry should build successfully."""
    entry = MonitorMetadataEntry(
        monitor_id="monitor_inventory_001",
        display_target_id="display_foundation_primary",
        metadata_role="foundation_primary_metadata",
        metadata_state="monitor_metadata_ready",
        display_role="foundation_primary_display",
        display_zone="foundation_main_zone",
        fallback_display_target_id="display_foundation_secondary",
        occupancy_class="foundation_primary_display",
        assignment_count=1,
        supports_foundation_panels=True,
        supports_operator_surfaces=False,
        multi_monitor_capable=True,
        operator_visible=True,
        description="Canonical foundation primary metadata.",
    )

    assert entry.metadata_role == "foundation_primary_metadata"
    assert entry.display_zone == "foundation_main_zone"


def test_monitor_metadata_entry_accepts_operator_metadata() -> None:
    """Operator metadata entry should build successfully."""
    entry = MonitorMetadataEntry(
        monitor_id="monitor_inventory_003",
        display_target_id="display_operator_interaction",
        metadata_role="operator_interaction_metadata",
        metadata_state="monitor_metadata_ready",
        display_role="operator_interaction_display",
        display_zone="operator_interaction_zone",
        fallback_display_target_id="display_operator_interaction",
        occupancy_class="operator_interaction_display",
        assignment_count=1,
        supports_foundation_panels=False,
        supports_operator_surfaces=True,
        multi_monitor_capable=True,
        operator_visible=True,
        description="Canonical operator interaction metadata.",
    )

    assert entry.metadata_role == "operator_interaction_metadata"
    assert entry.display_zone == "operator_interaction_zone"


def test_monitor_metadata_entry_rejects_zero_assignments() -> None:
    """Canonical monitor metadata must expose at least one assignment."""
    with pytest.raises(ValueError, match="assignment_count must be >= 1."):
        MonitorMetadataEntry(
            monitor_id="monitor_inventory_invalid",
            display_target_id="display_foundation_secondary",
            metadata_role="foundation_secondary_metadata",
            metadata_state="monitor_metadata_ready",
            display_role="foundation_secondary_display",
            display_zone="foundation_secondary_zone",
            fallback_display_target_id="display_foundation_primary",
            occupancy_class="foundation_secondary_display",
            assignment_count=0,
            supports_foundation_panels=True,
            supports_operator_surfaces=False,
            multi_monitor_capable=True,
            operator_visible=True,
            description="Invalid foundation secondary metadata.",
        )
