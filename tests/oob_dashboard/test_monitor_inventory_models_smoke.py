from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_models import (
    MonitorInventoryEntry,
)


def test_monitor_inventory_entry_accepts_foundation_monitor() -> None:
    """Foundation monitor inventory entry should build successfully."""
    entry = MonitorInventoryEntry(
        monitor_id="monitor_inventory_001",
        display_target_id="display_foundation_primary",
        monitor_role="foundation_primary_monitor",
        inventory_state="monitor_present",
        supports_foundation_panels=True,
        supports_operator_surfaces=False,
        multi_monitor_capable=True,
        operator_visible=True,
        description="Canonical foundation primary monitor.",
    )

    assert entry.monitor_role == "foundation_primary_monitor"
    assert entry.supports_foundation_panels is True
    assert entry.supports_operator_surfaces is False


def test_monitor_inventory_entry_accepts_operator_monitor() -> None:
    """Operator interaction monitor inventory entry should build successfully."""
    entry = MonitorInventoryEntry(
        monitor_id="monitor_inventory_003",
        display_target_id="display_operator_interaction",
        monitor_role="operator_interaction_monitor",
        inventory_state="monitor_present",
        supports_foundation_panels=False,
        supports_operator_surfaces=True,
        multi_monitor_capable=True,
        operator_visible=True,
        description="Canonical operator interaction monitor.",
    )

    assert entry.monitor_role == "operator_interaction_monitor"
    assert entry.supports_foundation_panels is False
    assert entry.supports_operator_surfaces is True


def test_monitor_inventory_entry_rejects_operator_monitor_without_operator_surface_support() -> None:
    """Operator interaction monitors must support operator surfaces."""
    with pytest.raises(
        ValueError,
        match="operator_interaction_monitor must support operator surfaces.",
    ):
        MonitorInventoryEntry(
            monitor_id="monitor_inventory_invalid",
            display_target_id="display_operator_interaction",
            monitor_role="operator_interaction_monitor",
            inventory_state="monitor_present",
            supports_foundation_panels=False,
            supports_operator_surfaces=False,
            multi_monitor_capable=True,
            operator_visible=True,
            description="Invalid operator interaction monitor.",
        )
